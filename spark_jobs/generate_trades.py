import json
import random
import string
import time
import uuid
from datetime import datetime, timedelta
from kafka import KafkaProducer





TOPIC = "trades.raw.v1"
BOOTSTRAP_SERVERS = "localhost:9092"

SYMBOLS = ["RY.TO", "TD.TO", "BNS.TO", "BMO.TO", "CM.TO"]
CURRENCIES = ["CAD", "USD", "EUR", "GBP"]  # CAD/USD valid, rest = invalid
BROKERS = ["BRK-001", "BRK-002", "BRK-011", "BRK-020"]




producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v:json.dumps(v).encode("utf-8")

)