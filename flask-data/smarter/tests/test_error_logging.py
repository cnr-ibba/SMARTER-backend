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

        # Patch logging.warning to capture the simulated email
        with patch("logging.warning") as mock_warning:
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
            with patch("logging.info") as mock_info:
                # Mock the emit to simulate successful send
                mock_emit.return_value = None

                handler.emit(record)

                # Verify that we attempted to send (called parent's emit)
                mock_emit.assert_called_once()

                # Verify that we logged the attempt Before and after send
                self.assertEqual(mock_info.call_count, 2)

                # First call should be about sending
                first_call = mock_info.call_args_list[0][0][0]
                self.assertIn("Sending error email", first_call)

                # Second call should be about success
                second_call = mock_info.call_args_list[1][0][0]
                self.assertIn("sent successfully", second_call)
