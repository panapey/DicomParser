import json
import os

from pydicom import dcmread


def write_json(path: str, data: dict) -> None:
    """
    Запись данных в json

    Args:
        path: название конечного файла
        data: словарь с данными
    """

    with open(path, 'w') as file:
        json.dump(data, file, indent=4)


def process_data(src_dir: str) -> dict[str, dict[str, str]]:
    """
    Обработка исходных данных и создание иерархии

    Args:
        src_dir: путь к исходным данным

    Returns:
        Словарь с соответствиями путей
    """

    data = {}
    for root, dirs, files in os.walk(src_dir):
        for filename in files:
            ds = dcmread(f'{root}/{filename}')
            del ds.PatientID

            path = f'end/{ds.StudyInstanceUID}/{ds.SeriesInstanceUID}'
            os.makedirs(path, exist_ok=True)

            ds.save_as(f'{path}/{ds.SOPInstanceUID}.dcm')

            data[filename] = {
                'src': f'{root}/{filename}',
                'end': f'{path}/{ds.SOPInstanceUID}.dcm'
            }
    return data


def main():
    write_json('paths.json', process_data('src'))


if __name__ == '__main__':
    main()
