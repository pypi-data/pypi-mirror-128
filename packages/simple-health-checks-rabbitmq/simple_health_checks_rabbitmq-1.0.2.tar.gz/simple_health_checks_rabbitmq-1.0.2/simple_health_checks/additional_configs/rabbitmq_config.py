from dynaconf import Validator

validators = [Validator("RABBITMQ_BROKER_URL", default="")]
