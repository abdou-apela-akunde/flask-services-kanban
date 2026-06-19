import requests


BASE_URL = "http://localhost:5004"


def main():
    with open("data/donnees_exemple.csv", "rb") as csv_file:
        response = requests.post(
            f"{BASE_URL}/upload/csv",
            files={"file": ("donnees_exemple.csv", csv_file, "text/csv")},
            timeout=10,
        )

    print("POST /upload/csv")
    print(response.status_code)
    print(response.json())

    response = requests.get(f"{BASE_URL}/upload/series", timeout=10)
    print("GET /upload/series")
    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    main()
