import random
import time
from datetime import datetime

# Voltage protection limits
NORMAL_VOLTAGE = 230.0
UNDER_VOLTAGE_LIMIT = 200.0
OVER_VOLTAGE_LIMIT = 250.0

# Number of abnormal readings required before tripping
FAULT_LIMIT = 3

breaker_status = "ON"
under_voltage_count = 0
over_voltage_count = 0


def read_voltage():
    """
    Simulate voltage sensor readings.

    For a real system, replace this with data from an
    appropriately isolated and rated voltage measurement circuit.
    """
    return random.uniform(180, 270)


def check_voltage(voltage):
    """Determine the voltage condition."""

    if voltage < UNDER_VOLTAGE_LIMIT:
        return "UNDER VOLTAGE"

    if voltage > OVER_VOLTAGE_LIMIT:
        return "OVER VOLTAGE"

    return "NORMAL"


def trip_breaker(reason):
    """Trip the protection breaker."""

    global breaker_status

    breaker_status = "TRIPPED"

    print("\n⚠ PROTECTION TRIPPED")
    print(f"Reason: {reason}")


def main():
    global under_voltage_count
    global over_voltage_count

    print("=" * 65)
    print("       OVERVOLTAGE & UNDERVOLTAGE PROTECTION")
    print("=" * 65)

    try:

        while True:

            if breaker_status == "TRIPPED":
                print("\nBreaker Status: TRIPPED")
                print("System stopped for safety.")
                break

            voltage = read_voltage()

            condition = check_voltage(voltage)

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            print("\n------------------------------------------")
            print(f"Time          : {timestamp}")
            print(f"Voltage       : {voltage:.2f} V")
            print(f"Condition     : {condition}")
            print(f"Breaker       : {breaker_status}")

            if condition == "UNDER VOLTAGE":

                under_voltage_count += 1
                over_voltage_count = 0

                print(
                    f"Under-voltage count: "
                    f"{under_voltage_count}/{FAULT_LIMIT}"
                )

                if under_voltage_count >= FAULT_LIMIT:
                    trip_breaker("UNDER VOLTAGE")

            elif condition == "OVER VOLTAGE":

                over_voltage_count += 1
                under_voltage_count = 0

                print(
                    f"Over-voltage count: "
                    f"{over_voltage_count}/{FAULT_LIMIT}"
                )

                if over_voltage_count >= FAULT_LIMIT:
                    trip_breaker("OVER VOLTAGE")

            else:

                under_voltage_count = 0
                over_voltage_count = 0
                print("System Status: NORMAL")

            print("------------------------------------------")

            time.sleep(3)

    except KeyboardInterrupt:

        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
