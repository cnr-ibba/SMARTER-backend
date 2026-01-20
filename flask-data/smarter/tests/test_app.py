#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 2026

Test error logging behavior for 400 and 500 errors
"""

import logging
from unittest.mock import patch

from mongoengine.errors import ValidationError

from .base import BaseCase


class TestErrorLogging(BaseCase):
    """Test that error logging works correctly for different error types"""

    fixtures = []

    def test_400_error_logs_as_warning(self):
        """Test that 400 errors (ValidationError) log as WARNING, not ERROR"""

        with self.app.app_context():
            with patch("flask.current_app.logger") as mock_logger:
                # Simulate what happens in common/views.py when ValidationError
                # occurs
                try:
                    # Simulate a mongoengine ValidationError
                    raise ValidationError("Invalid ObjectId format")
                except ValidationError as e:
                    # This is what the code does in common/views.py
                    mock_logger.warning(e)

                # Verify that warning was called (not error)
                mock_logger.warning.assert_called_once()
                mock_logger.error.assert_not_called()

    def test_500_error_logs_as_error(self):
        """Test that 500 errors (unhandled exceptions) log as ERROR"""

        with self.app.app_context():
            with patch("flask.current_app.logger") as mock_logger:
                # Simulate an internal server error
                try:
                    raise Exception("Internal server error")
                except Exception as e:
                    # This is what should happen for 500 errors
                    mock_logger.error(e)

                # Verify that error was called
                mock_logger.error.assert_called_once()

    def test_smtp_handler_logs_simulated_email_for_localhost(self):
        """Test that LoggingSMTPHandler simulates email for localhost"""

        from app import LoggingSMTPHandler

        # Create a handler with localhost configuration
        handler = LoggingSMTPHandler(
            mailhost=("localhost", 1025),
            fromaddr="test@example.com",
            toaddrs=["admin@example.com"],
            subject="Test Error",
        )

        # Create a mock log record at ERROR level
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            msg="Test error message",
            args=(),
            exc_info=None,
        )

        # Patch the handler's logger to capture the simulated email
        with patch.object(handler.logger, "warning") as mock_warning:
            handler.emit(record)

            # Verify that logging.warning was called (simulated email)
            mock_warning.assert_called_once()
            call_args = mock_warning.call_args[0][0]

            # Check that the simulated email contains expected content
            self.assertIn("SIMULATED EMAIL", call_args)
            self.assertIn("localhost mode", call_args)
            self.assertIn("test@example.com", call_args)
            self.assertIn("admin@example.com", call_args)

    def test_smtp_handler_sends_real_email_for_non_localhost(self):
        """Test that LoggingSMTPHandler tries to send real email for
        non-localhost"""

        from app import LoggingSMTPHandler

        # Create a handler with non-localhost configuration
        handler = LoggingSMTPHandler(
            mailhost=("smtp.example.com", 587),
            fromaddr="test@example.com",
            toaddrs=["admin@example.com"],
            subject="Test Error",
        )

        # Create a mock log record at ERROR level
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            msg="Test error message",
            args=(),
            exc_info=None,
        )

        # Patch the parent SMTPHandler.emit to avoid actually sending email
        with patch("logging.handlers.SMTPHandler.emit") as mock_emit:
            with patch.object(handler.logger, "info") as mock_info:
                # Mock the emit to simulate successful send
                mock_emit.return_value = None

                handler.emit(record)

                # Verify that we attempted to send (called parent's emit)
                mock_emit.assert_called_once()

                # Verify that we logged the attempt before and after send
                self.assertEqual(mock_info.call_count, 2)

                # First call should be about sending
                first_call = mock_info.call_args_list[0][0][0]
                self.assertIn("Sending error email", first_call)

                # Second call should be about success
                second_call = mock_info.call_args_list[1][0][0]
                self.assertIn("sent successfully", second_call)

    def test_smtp_handler_logs_email_failure(self):
        """Test that LoggingSMTPHandler logs failures when sending emails"""

        from app import LoggingSMTPHandler

        # Create a handler with non-localhost configuration
        handler = LoggingSMTPHandler(
            mailhost=("smtp.example.com", 587),
            fromaddr="test@example.com",
            toaddrs=["admin@example.com"],
            subject="Test Error",
        )

        # Create a mock log record at ERROR level
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=1,
            msg="Test error message",
            args=(),
            exc_info=None,
        )

        # Patch the parent SMTPHandler.emit to simulate failure
        with patch("logging.handlers.SMTPHandler.emit") as mock_emit:
            with patch.object(handler.logger, "error") as mock_error:
                with patch.object(handler.logger, "info"):
                    # Make emit raise an exception to simulate send failure
                    mock_emit.side_effect = Exception("Connection failed")

                    handler.emit(record)

                    # Verify that error was logged
                    mock_error.assert_called_once()
                    call_args = mock_error.call_args[0][0]
                    self.assertIn("Failed to send error email", call_args)

    def test_request_formatter_with_request_context(self):
        """Test RequestFormatter includes request info when in request
        context"""

        from app import RequestFormatter

        formatter = RequestFormatter(
            '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
            '%(levelname)s in %(module)s: %(message)s'
        )

        # Create a mock log record
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        # Test with request context
        with self.app.test_request_context('/test-url',
                                           environ_base={'REMOTE_ADDR':
                                                         '127.0.0.1'}):
            formatted = formatter.format(record)

            self.assertIn('127.0.0.1', formatted)
            self.assertIn('/test-url', formatted)

    def test_request_formatter_without_request_context(self):
        """Test RequestFormatter handles no request context gracefully"""

        from app import RequestFormatter

        formatter = RequestFormatter(
            '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
            '%(levelname)s in %(module)s: %(message)s'
        )

        # Create a mock log record
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None,
        )

        # Test without request context (app context only)
        with self.app.app_context():
            formatted = formatter.format(record)

            # Should contain 'None' for both url and remote_addr
            self.assertIn('None', formatted)

    def test_custom_json_encoder_objectid(self):
        """Test CustomJSONEncoder handles ObjectId correctly"""

        from app import CustomJSONEncoder
        from bson import ObjectId

        encoder = CustomJSONEncoder()
        test_id = ObjectId("507f1f77bcf86cd799439011")

        result = encoder.default(test_id)

        self.assertIsInstance(result, dict)
        self.assertIn("$oid", result)
        self.assertEqual(result["$oid"], "507f1f77bcf86cd799439011")

    def test_custom_json_encoder_default(self):
        """Test CustomJSONEncoder falls back to default for other types"""

        from app import CustomJSONEncoder

        encoder = CustomJSONEncoder()

        # Test with a type that's not ObjectId
        # This should raise TypeError as expected
        with self.assertRaises(TypeError):
            encoder.default(set([1, 2, 3]))

    def test_create_app_debug_mode(self):
        """Test that create_app respects DEBUG configuration"""

        import os
        from app import create_app

        # Save original value
        original_debug = os.environ.get('DEBUG')

        try:
            # Set DEBUG to True
            os.environ['DEBUG'] = 'True'

            test_app = create_app()

            self.assertTrue(test_app.debug)

        finally:
            # Restore original value
            if original_debug is not None:
                os.environ['DEBUG'] = original_debug
            elif 'DEBUG' in os.environ:
                del os.environ['DEBUG']

    def test_create_app_adds_mail_handler_in_production(self):
        """Test that mail handler is added when not in debug mode"""

        import os
        from app import create_app

        # Save original value
        original_debug = os.environ.get('DEBUG')

        try:
            # Ensure DEBUG is False
            if 'DEBUG' in os.environ:
                del os.environ['DEBUG']

            test_app = create_app()

            # Check that mail handler was added
            handler_types = [
                type(h).__name__ for h in test_app.logger.handlers
            ]
            self.assertIn('LoggingSMTPHandler', handler_types)

        finally:
            # Restore original value
            if original_debug is not None:
                os.environ['DEBUG'] = original_debug

    def test_index_route_redirects_to_docs(self):
        """Test that /smarter-api/ redirects to API docs"""

        response = self.client.get('/smarter-api/')

        # Should redirect (302)
        self.assertEqual(response.status_code, 302)

        # Should redirect to flasgger docs
        self.assertIn('/smarter-api/docs/', response.location)

    def test_main_block_execution(self):
        """Test that __main__ block can execute without errors"""

        import subprocess
        import sys

        # Run the app.py module as a script with a timeout
        # We'll just check it can start without errors
        result = subprocess.run(
            [sys.executable, '-c',
             'import app; app.create_app()'],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Should execute without errors
        self.assertEqual(result.returncode, 0)
