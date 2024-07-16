from confluent_kafka import Producer, KafkaException
import json
import time
import requests
from bs4 import BeautifulSoup

# Kafka configuration
topic = 'kafka-topic'
file_path = 'data.json'
conf = {'bootstrap.servers': 'kafka:9092'}
producer = Producer(conf)


class Request:
    @staticmethod
    def scrape_data():
        url = 'https://scrapeme.live/shop/Bulbasaur/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        products = []
        
        name_tag = soup.find('h1', class_='product_title entry-title')
        name = name_tag.text if name_tag else "No name available"

        price_tag = soup.find('p', class_='price')
        price = price_tag.text if price_tag else "No price available"

        description_tag = soup.find('div', class_='woocommerce-product-details__short-description')
        description = description_tag.text if description_tag else "No description available"

        stock_tag = soup.find('p', class_='stock in-stock')
        stock = stock_tag.text if stock_tag else "Stock information not available"

        product = {
            'name': name,
            'price': price,
            'description': description,
            'stock': stock
        }
        products.append(product)
        
        return products

        
class Kafka:
    @staticmethod
    def producer(data):
        for item in data:
            try:
                producer.produce(topic, json.dumps(item).encode('utf-8'))
                print(f"Produced message: {item}")
                time.sleep(1)  
            except KafkaException as e:
                print(f"Failed to produce message: {e}")

        producer.flush()

    @staticmethod
    def producer_with_file(data):
        with open(file_path, 'w') as file:
            for item in data:
                try:
                    
                    producer.produce(topic, json.dumps(item).encode('utf-8'))
                    print(f"Produced message: {item}")

                    file.write(json.dumps(item) + '\n')

                    time.sleep(1)  
                except KafkaException as e:
                    print(f"Failed to produce message: {e}")

        producer.flush()

    @staticmethod
    def try_to_write(item):

        try:
            producer.produce(topic, json.dumps(item).encode('utf-8'))
            print(f"Produced message: {item}")
            time.sleep(1)  
        except KafkaException as e:
            print(f"Failed to produce message: {e}")

        producer.flush()

if __name__ == "__main__":

    Kafka.try_to_write({"message": "deneme"})

    data = Request.scrape_data()

    if data:
        
        Kafka.producer(data)

        Kafka.producer_with_file(data)

    else:
        print("Error! No data...")
