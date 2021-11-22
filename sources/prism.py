import dataRetrieval
import dataTransformation
import dataLoader
import argparse


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-hospital', help="Comma separated list of hospitals. eg: 'Interfaith,Wyckoff'.")
    args=parser.parse_args()
    hospitals = args.hospital.split(',')
    for hospital in hospitals:
        hospital = hospital.strip().lower()
        dataRetrieval.run(hospital=hospital)
        transformedData = dataTransformation.run(hospital=hospital)
        dataLoader.run(*transformedData, hospital=hospital)


if __name__ == '__main__':
    main()