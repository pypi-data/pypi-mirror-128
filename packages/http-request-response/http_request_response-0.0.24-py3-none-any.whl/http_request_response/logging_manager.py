import requests


class AWSCloudWatchLogger:
    @staticmethod
    def log_info(app, msg):
        try:
            app.aws_cloud_watch_info_logger.info(msg)

        except:
            pass

    @staticmethod
    def log_exception(app, msg):
        try:
            app.aws_cloud_watch_exc_logger.exception(msg)

        except:
            pass


class SlackLogger:
    @staticmethod
    def log_info(app, msg):
        try:
            url = app.config['SLACK_INFO_API_URL']
            payload = {'text': msg}
            requests.post(url=url, json=payload)

        except:
            pass

    @staticmethod
    def log_exception(app, msg):
        try:
            url = app.config['SLACK_EXC_API_URL']
            payload = {'text': msg}
            requests.post(url=url, json=payload)

        except:
            pass


class LoggingManager:
    @staticmethod
    def log_info(app, msg):
        AWSCloudWatchLogger.log_info(app, msg)
        SlackLogger.log_info(app, msg)

    @staticmethod
    def log_exception(app, msg):
        AWSCloudWatchLogger.log_exception(app, msg)
        SlackLogger.log_exception(app, msg)
