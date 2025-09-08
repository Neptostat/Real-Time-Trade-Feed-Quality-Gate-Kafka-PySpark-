import os, json, random, time
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from confluent_kafka import Producer
from trade_schema import Trade

BROKER = os.getenv("BROKER", "localhost:9092")
TOPIC = os.getenv("TOPIC_TRADES", "trades.raw.v1")
EPS = int(os.getenv("EVENTS_PER_SEC", "20"))

SYMBOLS = []
with open(os.path.join(os.path.dirname(__file__), "symbols.csv")) as f:
    for line in f:
        sym = line.strip().split(",")[0]
        if sym and sym != "symbol":
            SYMBOLS.append(sym)

p = Producer({
    "bootstrap.servers": BROKER,
    "enable.idempotence": True,
    "acks": "all",
})

venues = ["NYSE","NASDAQ","CBOE"]
sides = ["BUY","SELL"]

print(f"Producing to {BROKER} topic={TOPIC} eps={EPS}")

try:
    while True:
        ts = datetime.now(timezone.utc)
        for _ in range(EPS):
            symbol = random.choice(SYMBOLS)
            price = round(random.uniform(5, 500), 2)
            qty = random.choice([10,25,50,100,200,500])
            side = random.choice(sides)
            t = Trade(
                trade_id=str(uuid4()),
                ts_event=ts,
                symbol=symbol,
                side=side,
                price=price,
                quantity=qty,
                venue=random.choice(venues),
                trader_id=f"tr{random.randint(1,50):03d}"
            )
            p.produce(TOPIC, key=t.symbol.encode(), value=t.to_json())
        p.flush()
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped.")