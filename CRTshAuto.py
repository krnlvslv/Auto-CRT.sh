import requests
    

def get_certificates(domain):
    response = requests.get(f'https://crt.sh/?q={domain}&output=json')
    if response.status_code == 200:
        try:
            return response.json()
        except:
            print("Ошибка при парсинге JSON ответа")
    else:
        print(f'Запрос завершился с ошибкой: {response.status_code}')


def save_certificates(certificates, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for certificate in certificates:
            certificate_info = (
                f'crt.sh ID: {certificate.get("id")}\n'
                f'Logged At: {certificate.get("entry_timestamp")}\n'
                f'Not Before: {certificate.get("not_before")}\n'
                f'Not After: {certificate.get("not_after")}\n'
                f'Common Name: {certificate.get("common_name")}\n'
                f'Matching Identities: {certificate.get("name_value")}\n'
                f'Issuer Name: {certificate.get("issuer_name")}\n'
                f'\n'
                )
            file.write(certificate_info)


def find_subdomains(certificates):
    subdomains = set()
    for certificate in certificates:
        sd = certificate.get("name_value", "")
        if sd:
            for domain in sd.split("\n"):
                if domain.strip():
                    subdomains.add(domain.strip())
    return sorted(subdomains)


while True:
    choose = input("\nВведите '1' для поиска поддоменов, '2' для получения сертификатов домена, '3' для выхода из программы: ")
    if choose == "3":
        break
    elif choose == "2":
        domain = input("Введите домен: ")
        certificates = get_certificates(domain)
        if certificates:
            filename = f'{domain}_certificates.txt'
            save_certificates(certificates, filename)
            print(f'Сертификаты сохранены в файл {filename}')
        else:
            print("Не удалось получить сертификаты")
    elif choose == "1":
        domain = input("Введите домен: ")
        basic_domain = domain
        certificates = get_certificates(domain)
        if certificates:
            subdomains = find_subdomains(certificates)
            if subdomains:
                count = len(subdomains)
                print(f'Найдено {count - 1} поддоменов {domain}:\n')
                for subdomain in subdomains:
                    if subdomain != basic_domain:
                        print(subdomain)
            else:
                print("Поддомены не найдены")
        else:
            print("Поддомены не найдены")
