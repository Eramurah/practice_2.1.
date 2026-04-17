import struct
import time


def parse_binary_file(file_path):
    header_fmt = "<4sHI"
    header_size = struct.calcsize(header_fmt)

    # Запись: Q (uint64), I (uint32), h (int16), B (uint8)
    record_fmt = "<QIhB"
    record_size = struct.calcsize(record_fmt)

    records = []

    try:
        with open(file_path, "rb") as f:
            header_data = f.read(header_size)
            if len(header_data) < header_size:
                return "Ошибка: Некорректный заголовок"

            sig, ver, count = struct.unpack(header_fmt, header_data)
            if sig != b'DATA':
                return "Ошибка: Неверная сигнатура"


            for _ in range(count):
                record_data = f.read(record_size)
                if len(record_data) < record_size:
                    break

                ts, record_id, temp_raw, status = struct.unpack(record_fmt, record_data)

                records.append({
                    "timestamp": ts,
                    "id": record_id,
                    "Температура (Цельсий)": temp_raw / 100.0,
                    "status_flag": hex(status)
                })

            return {"version": ver, "data": records}

    except Exception as e:
        return f"Произошла ошибка: {e}"


def create_test_file(filename):
    header_fmt = "<4sHI"  # Сигнатура, Версия, Кол-во записей
    record_fmt = "<QIhB"  # Timestamp, ID, Temp*100, Status


    records_data = [
        (int(time.time()), 1, 2550, 0b00000001), # timestamp (в сек.), id, temp_raw, status
        (int(time.time()) + 60, 2, -1015, 0b00000010), # timestamp (в сек.), id, temp_raw, status
        (int(time.time()) + 120, 3, 0, 0b11000000) # timestamp (в сек.), id, temp_raw, status
    ]

    header_bytes = struct.pack(header_fmt, b'DATA', 1, len(records_data))

    try:
        with open(filename, "wb") as f:
            f.write(header_bytes)


            for rec in records_data:
                f.write(struct.pack(record_fmt, *rec))

        print(f"Файл '{filename}' создан. Записей: {len(records_data)}")
    except IOError as e:
        print(f"Ошибка записи: {e}")


if __name__ == "__main__":
    create_test_file("test_data.bin")
    print(parse_binary_file("test_data.bin"))