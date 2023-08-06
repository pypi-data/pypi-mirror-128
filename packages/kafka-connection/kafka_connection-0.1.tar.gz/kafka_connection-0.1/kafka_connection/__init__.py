import json
import os
from concurrent import futures
import requests
from confluent_kafka import Consumer
from confluent_kafka import Producer

from logger.log import Log
from util.utils import Utils

log = Log()


class KafkaConnection:

    def __init__(self):
        self.utils_object = Utils()
        self.kafka_config = {}

    def get_kafka_configuration(self):
        remove_list = ['value.serializer', 'key.serializer', 'kafka.request.required.ack',
                       'max.block.ms', 'max.in.flight.requests.per.connection', 'key.deserializer',
                       'value.deserializer', 'group.id']
        try:
            url = str(os.getenv('MDS_BASE_URL')) + "/api/v1/configuration/kafka"
            resp = requests.get(url)
            kafka_config_json = json.loads(resp.content)
            if self.utils_object.get_json_value(kafka_config_json, 'success'):
                data = self.utils_object.get_json_value(kafka_config_json, 'data')
                if self.utils_object.iskey_validate(data, 'confType') and self.utils_object.iskey_validate(data,
                                                                                                           'confDetails'):
                    if self.utils_object.get_json_value(data, 'confType') == 'Kafka':
                        confDetails = data['confDetails']
                        for key in confDetails:
                            if key not in remove_list:
                                self.kafka_config[key] = confDetails[key]
                        self.kafka_config['max.in.flight.requests.per.connection'] = '1000000'
                        self.kafka_config['message.max.bytes'] = '1000000000'
                        self.kafka_config['fetch.message.max.bytes'] = '1000000000'
                        self.kafka_config['queue.buffering.max.ms'] = '900000'
                        self.kafka_config['max.poll.interval.ms'] = '86400000'
                        self.kafka_config["linger.ms"] = '1000'
                        self.kafka_config["group.id"] = os.getenv('COMPONENT_INST_ID')
                        self.kafka_config["compression.type"] = "gzip"
                        self.kafka_config['session.timeout.ms'] = '60000'
                        # self.kafka_config['request.timeout.ms'] = '360000'
                        # self.kafka_config['heartbeat.interval.ms'] = '100'
                        #self.kafka_config['partition.assignment.strategy'] = 'roundrobin'

                    ############## SSL Config #################

                        protocol = os.getenv('KAFKA_PROTOCOL')
                        if protocol is not None:
                            secretFiles = os.getenv('MOUNT_SECRET_FILES')
                            secretFiles_json = json.loads(secretFiles)
                            path = secretFiles_json[0]['path']
                            # self.kafka_config['bootstrap.servers'] = '192.168.45.60:9093,192.168.45.60:9092,192.168.45.60:9091'
                            self.kafka_config['security.protocol'] = 'SSL'
                            self.kafka_config['ssl.ca.location'] = path+"/"+"CARoot.pem"
                            self.kafka_config['ssl.certificate.location'] = path+"/"+"certificate.pem"
                            self.kafka_config["ssl.key.location"] = path+"/"+"key.pem"
                            # self.kafka_config['security.protocol'] = 'SSL'
                            # self.kafka_config["ssl.ca.location"] = 'E:/kafka_file/CARoot.pem'
                            # self.kafka_config["ssl.certificate.location"] = 'E:/kafka_file/certificate.pem'
                            # self.kafka_config["ssl.key.location"] = 'E:/kafka_file/key.pem'


        except Exception as e:
            log.exception(KafkaConnection.__name__, KafkaConnection.get_kafka_configuration.__name__, str(e))
        finally:
            pass
        return self.kafka_config

    def getkafka_producer(self):
        kafka_producer = None
        try:
            if len(self.kafka_config) == 0:
                self.get_kafka_configuration()
            kafka_producer = Producer(self.kafka_config)
        except Exception as e:
            log.exception(KafkaConnection.__name__, KafkaConnection.getkafka_producer.__name__, str(e))
        finally:
            pass
        return kafka_producer

    def getkafka_consumer(self):
        kafka_consumer = None
        try:
            if len(self.kafka_config) == 0:
                self.get_kafka_configuration()
            kafka_consumer = Consumer(self.kafka_config)
        except Exception as e:
            log.exception(KafkaConnection.__name__, KafkaConnection.getkafka_consumer.__name__, str(e))
        finally:
            pass
        return kafka_consumer

    def producedata(self, topic, datalists):
        try:
            p = self.getkafka_producer()

            def delivery_callback(err, msg):
                if err is not None:
                    print('Message delivery failed: {}'.format(err))

            for data_list in datalists:
                try:
                    if isinstance(data_list, dict):
                        p.produce(topic, value=json.dumps(data_list).encode('utf-8'), callback=delivery_callback)
                    else:
                        p.produce(topic, value=str(data_list).encode('utf-8'), callback=delivery_callback)
                    # result = future.get(timeout=60)
                    # print(result)
                    p.poll(0)
                    # print(data_list)
                except Exception as e:
                    log.exception(KafkaConnection.__name__, KafkaConnection.producedata.__name__, str(e))
            p.flush()
        except Exception as e:
            log.exception(KafkaConnection.__name__, KafkaConnection.producedata.__name__, str(e))

    def produceBatchdata(self, topic, datalists):
        try:
            if len(self.kafka_config) == 0:
                self.get_kafka_configuration()
            p = Producer(self.kafka_config)
            for datalist in datalists:
                try:
                    if isinstance(datalist, dict):
                        p.produce(topic, value=json.dumps(datalist).encode('utf-8'))
                    else:
                        p.produce(topic, value=str(datalist).encode('utf-8'))
                    # p.poll(0)
                except Exception as e:
                    log.exception(KafkaConnection.__name__, KafkaConnection.producedata.__name__, str(e))
            p.flush()
        except Exception as e:
            log.exception(KafkaConnection.__name__, KafkaConnection.producedata.__name__, str(e))
        finally:
            del datalists

    def run_threadfun(self, data_list, topic):
        try:
            chunks = 10
            with futures.ProcessPoolExecutor() as executor:
                for i in range(0, len(data_list), chunks):
                    executor.submit(self.producedata, *[topic, data_list[i:i + chunks]])
        except Exception as e:
            log.exception(KafkaConnection.__name__, KafkaConnection.run_threadfun.__name__, str(e))
        finally:
            del data_list

    def run_fun(self, data_list, topic):
        try:
            self.producedata(topic, data_list)

        except Exception as e:
            log.exception(KafkaConnection.__name__, KafkaConnection.run_threadfun.__name__, str(e))
        finally:
            del data_list


if __name__ == '__main__':
    pass
