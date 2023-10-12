# ------------------------ Importing modules ------------------------ #
#! -------------------      all code no touchy     -------------------#
import requests  # Default
import os  # Default
import sys  # Default
import random  # Default
import time  # Default
import readline  # Default
import re  # Default
import uuid  # Default
import socket  # Default
import platform  # Default
import psutil  # pip install psutil
import bs4  # pip install beautifulsoup4
import phonenumbers  # pip install phonenumbers
from mac_vendor_lookup import MacLookup # pip install mac-vendor-lookup
import whois  # pip install python-whois
import dns.resolver  # pip install dnspython
import validate_email_address  # pip install validate_email_address
from colorama import Style, Fore  # pip install colorama

# pip install requests os sys random time readline re uuid socket platform psutil beautifulsoup4 phonenumbers mac-vendor-lookup python-whois dnspython validate_email_address colorama

# ------------------------- Global variables ------------------------ #
avaliable_commands = [
    "change",
    "check",
    "clear",
    "dork",
    "dns",
    "exit",
    "exp",
    "help",
    "info",
    "ip",
    "mac",
    "number",
    "name",
    "email",
    "quit",
    "save",
    "shell",
    "whois",
    "coordinate",
]
prv_op = ""
full_cmd = ""
silent_mode = False


# ------------------------ Scanner functions ------------------------ #
# TODO: Add Address lookup
# TODO: Add Familytree lookup
# TODO: Add Court case lookup
# ?------------------------ username function ------------------------ #
def username_lookup(username):
    # Global variables
    global prv_op
    prv_op = '' # Resetting previous output

    # Checking internet connection
    printit(f'    [+] Verifying internet connection...', coledt=[1, 49, 93], space_down=True)
    if not check_connection():
        printit('    > Internet connection not available!', coledt=[1, 49, 91], space_down=True)
        return False

    # Information gathering about the username
    printit(f'    [+] Grathering information about \33[1;49;96m{username}\33[1;49;93m...', coledt=[1, 49, 93], space_down=True)
    prv_op += f'    \33[1;49;93m[#] Reverse username lookup for \33[1;49;96m{username}\33[1;49;93m:\033[0m'+'\n\n'

    # Validating username (no spaces)
    if ' ' in username:
        printit('    > Invalid username!', coledt=[1, 49, 91], space_down=True)
        return False

    # Headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
    }
    
    # https://www.idcrawl.com/u/<username>
    try:
        response = requests.get('https://www.idcrawl.com/u/'+username, timeout=10, headers=headers)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        info_dict = {}
        soup = soup.find('div', {'class': 'gl-page-content col-md-8 col-sm-12 col-xs-12'})

        # save h2 and h3 tags in dictionary (h2 as key and h3 as value)
        for h2 in soup.find_all('h2'):
            try:
                # if there is `Not Taken` text inside the same div as h2 then skip it !!NEED_TO_FIX_IT!!
                if 'Not Taken' in h2.findNext('p').text:
                    continue
                if 'Email Addresses' in h2 or 'Secret Profiles' in h2: 
                    continue
                info_dict[str(h2).split('</i>')[1].split('</h2>')[0]] = h2.findNext('h3').text
            except:
                pass
        if info_dict:
            final_output = f'''
    ┌──────────────────────────────────────────────────────┐
    | Scanned Username: \33[1;49;96m{username+' '*int(34-len(str(username)))}\033[0m |
    |------------------------------------------------------|
    | INFORMATION         | DESCRIPTION                    |
    |------------------------------------------------------|'''

            for site, username in info_dict.items():
                site = str(site)+' '*int(19-len(str(site)))
                username = str(username)+' '*int(30-len(str(username)))
                final_output += f'''\n    | \33[1;49;97m{site}\033[0m | {username} |'''

            final_output += f'''\n    └──────────────────────────────────────────────────────┘'''

            print(final_output)
            prv_op += final_output+'\n'
            return True

        else:
            final_output = f'''
    ┌──────────────────────────────────────────────────────┐
    | Scanned Username: \33[1;49;96m{username+' '*int(34-len(str(username)))}\033[0m |
    |------------------------------------------------------|
    | INFORMATION         | DESCRIPTION                    |
    |------------------------------------------------------|
    | \33[1;49;91mFailed to Fetch information from server!\033[0m             |
    └──────────────────────────────────────────────────────┘
        '''
            print(final_output)
            prv_op += final_output+'\n'
            return False
    except Exception as e:
        print(e)
# ?------------------------ username function ------------------------ #
# ?------------------------ coordinate function ------------------------ #
def generate_map_urls(latitude, longitude):

    printit(f'    [+] Verifying internet connection...', coledt=[1, 49, 93], space_down=True)
    if not check_connection():
        printit('    > Internet connection not available!', coledt=[1, 49, 91], space_down=True)
        return False

    map_urls = f"""
    \33[1;49;93m[+] Searching for coordinates: \33[1;49;96m{latitude}, {longitude}\33[1;49;93m on various platforms:
        \33[1;49;92m> "Google Map": f"https://www.google.com/maps/@?api=1&map_action=map&center={latitude},{longitude}&zoom=18&basemap=roadmap",
        > "Google Sat": f"https://www.google.com/maps/@?api=1&map_action=map&center={latitude},{longitude}&zoom=18&basemap=satellite",
        > "Google Street": f"https://www.google.com/maps/@{latitude},{longitude},3a,90y/data=!3m6!1e1!3m4!1sLUqESS-jkIaAosYy4iRd5w!2e0!7i16384!8i8192?entry=ttu",
        > "Google Street (N)": f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={latitude},{longitude}&heading=0&pitch=0&fov=90",
        > "Google Street (E)": f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={latitude},{longitude}&heading=90&pitch=0&fov=90",
        > "Google Street (S)": f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={latitude},{longitude}&heading=180&pitch=0&fov=90",
        > "Google Street (W)": f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={latitude},{longitude}&heading=270&pitch=0&fov=90",
        > "Bing Map": f"https://www.bing.com/maps?&cp={latitude}~{longitude}&lvl=20",
        > "Bing Sat": f"https://www.bing.com/maps?cp={latitude}~{longitude}&lvl=20&sty=a",
        > "Bing Sat (N)": f"https://www.bing.com/maps?cp={latitude}~{longitude}&lvl=20&sty=o&w=100%&dir=0",
        > "Bing Sat (E)": f"https://www.bing.com/maps?cp={latitude}~{longitude}&lvl=20&sty=o&w=100%&dir=90",
        > "Bing Sat (S)": f"https://www.bing.com/maps?cp={latitude}~{longitude}&lvl=20&sty=o&w=100%&dir=180",
        > "Bing Sat (W)": f"https://www.bing.com/maps?cp={latitude}~{longitude}&lvl=20&sty=o&w=100%&dir=270",
        > "Bing Street (N)": f"https://www.bing.com/maps?cp={latitude}~{longitude}&lvl=20&dir=0&pi=0&style=x",
        > "Bing Street (E)": f"https://www.bing.com/maps?cp={latitude}~{longitude}&lvl=20&dir=90&pi=0&style=x",
        > "Bing Street (S)": f"https://www.bing.com/maps?cp={latitude}~{longitude}&lvl=20&dir=180&pi=0&style=x",
        > "Bing Street (W)": f"https://www.bing.com/maps?cp={latitude}~{longitude}&lvl=20&dir=270&pi=0&style=x",
        > "Zoom Earth": f"https://zoom.earth/#view={latitude},{longitude},20z",
        > "Here Sat": f"https://www.here.com/?map={latitude},{longitude},20,satellite",
        > "Yandex Sat": f"https://zoom.earth/#view={latitude},{longitude},20z",
        > "Descartes": f"https://search.descarteslabs.com/?layer=naip_v2_rgb_2014-2015#lat={latitude}&lng={longitude}&skipTut=true&zoom=20",
        > "Wikimapia": f"http://wikimapia.org/#lang=en&lat={latitude}&lon={longitude}&z=20",
        > "Snapchat": f"https://map.snapchat.com/@{latitude},{longitude},20.00z",
        > "Mapillary": f"https://www.mapillary.com/app/?lat={latitude}&lng={longitude}&z=18&p=&mapStyle=Mapillary+satellite&menu=false",
        > "Karta": f"https://kartaview.org/map/@{latitude},{longitude},18z",
        > "Land Viewer": f"https://eos.com/landviewer/?lat={latitude}&lng={longitude}&z=11",
        > "Apple Maps": f"https://satellites.pro/USA_map#{latitude},{longitude},18",
        > "AcreValue": f"https://www.acrevalue.com/map/?lat={latitude}&lng={longitude}&zoom=17",
        \033[0m"""
    return map_urls
# ?------------------------ coordinate function ------------------------ #
# ?------------------------ name function ------------------------ #
def reverse_name_lookup(first_name, last_name, city, state):

    printit(f'    [+] Verifying internet connection...', coledt=[1, 49, 93], space_down=True)
    if not check_connection():
        printit('    > Internet connection not available!', coledt=[1, 49, 91], space_down=True)
        return False

    state_abbreviations = {
        "alabama": "AL",
        "alaska": "AK",
        "arizona": "AZ",
        "arkansas": "AR",
        "california": "CA",
        "colorado": "CO",
        "connecticut": "CT",
        "delaware": "DE",
        "florida": "FL",
        "georgia": "GA",
        "hawaii": "HI",
        "idaho": "ID",
        "illinois": "IL",
        "indiana": "IN",
        "iowa": "IA",
        "kansas": "KS",
        "kentucky": "KY",
        "louisiana": "LA",
        "maine": "ME",
        "maryland": "MD",
        "massachusetts": "MA",
        "michigan": "MI",
        "minnesota": "MN",
        "mississippi": "MS",
        "missouri": "MO",
        "montana": "MT",
        "nebraska": "NE",
        "nevada": "NV",
        "new hampshire": "NH",
        "new jersey": "NJ",
        "new mexico": "NM",
        "new york": "NY",
        "north carolina": "NC",
        "north dakota": "ND",
        "ohio": "OH",
        "oklahoma": "OK",
        "oregon": "OR",
        "pennsylvania": "PA",
        "rhode island": "RI",
        "south carolina": "SC",
        "south dakota": "SD",
        "tennessee": "TN",
        "texas": "TX",
        "utah": "UT",
        "vermont": "VT",
        "virginia": "VA",
        "washington": "WA",
        "west virginia": "WV",
        "wisconsin": "WI",
        "wyoming": "WY",
    }

    # Function to get the abbreviation for a given state name
    def get_state_abbreviation(state_name):
        return state_abbreviations.get(state_name.lower(), "Unknown")

    # Replace spaces in the first and last name with hyphens to match the URL format
    formatted_first_name = first_name.replace(" ", "-")
    formatted_last_name = last_name.replace(" ", "-")

    # Replace hyphens in the city name with spaces
    formatted_city = city.replace("-", "%20")

    formatted_state = state_abbreviations.get(state.lower(), "unknown")

    name_url1 = f"""
    \33[1;49;93m[+] Searching for \33[1;49;96m{formatted_first_name}, {formatted_last_name}\33[1;49;93m on various platforms:
        \33[1;49;92m> Most Reliable: https://www.usphonebook.com/{formatted_first_name}-{formatted_last_name}/{state.lower()}/{city.lower()}
        > https://thatsthem.com/name/{formatted_first_name}-{formatted_last_name}/{city}-{formatted_state}
        > https://www.fastpeoplesearch.com/name/{formatted_first_name}-{formatted_last_name}_{city}-{formatted_state}
        > https://www.truepeoplesearch.com/results?name={formatted_first_name}%20{formatted_last_name}&citystatezip={formatted_city},%20{formatted_state}
        > https://nuwber.com/search?name={formatted_first_name}%20{formatted_last_name}
        > https://www.familytreenow.com/search/genealogy/results?first={formatted_first_name}&last={formatted_last_name}
        > https://www.intelius.com/people-search/{formatted_first_name}-{formatted_last_name}
        > https://radaris.com/p/{formatted_first_name}/{formatted_last_name}/
        > https://www.cyberbackgroundchecks.com/people/{formatted_first_name}-{formatted_last_name}
        > https://www.searchpeoplefree.com/find/{formatted_first_name}-{formatted_last_name}
        > https://www.spokeo.com/{formatted_first_name}-{formatted_last_name}
        > https://www.advancedbackgroundchecks.com/names/{formatted_first_name}-{formatted_last_name}
        > https://www.peoplesearchnow.com/person/{formatted_first_name}-{formatted_last_name}
        > https://webmii.com/people?n=%22{formatted_first_name}%20{formatted_last_name}%22
        > https://www.addresses.com/people/{formatted_first_name}-{formatted_last_name}
        \033[0m"""

    return name_url1


# ?------------------------ name function ------------------------ #
# ?------------------------ email function ------------------------ #
def email_lookup(email):
    import re
    import validate_email_address

    domain_pattern = r"@(.+)$"

    def get_service_provider(email):

        printit(f'    [+] Verifying internet connection...', coledt=[1, 49, 93], space_down=True)
        if not check_connection():
            printit('    > Internet connection not available!', coledt=[1, 49, 91], space_down=True)
            return False

        match = re.search(domain_pattern, email)

        if match:
            domain = match.group(1)
            parts = domain.split(".")
            if len(parts) >= 2:
                service_provider = ".".join(parts[-2:])
                return service_provider
        return None

    email_username = email.split("@")[0]
    validate_email = validate_email_address.validate_email(email)
    print(f"    [+] Validating email address {email}...")
    time.sleep(0.5)
    service_provider = get_service_provider(email)
    if validate_email:
        print(f"    [+]\033[1;49;32m Email Address Validated")
        time.sleep(0.5)
        final_output = f"""
    ┌──────────────────────────────────────────────────────┐
    | Scanned Email Address: \33[1;49;96m{email}\033[0m |
    |------------------------------------------------------|
    | INFORMATION         | DESCRIPTION                    |
    |------------------------------------------------------|
    | \33[1;49;97mPossible\033[0m            | {validate_email} |
    | \33[1;49;97mValid\033[0m               | {validate_email} |
    |------------------------------------------------------|
    | \33[1;49;97mService Provider\033[0m    | {service_provider} |
    | \33[1;49;97mUsername\033[0m            | {email_username} |
    └──────────────────────────────────────────────────────┘
        """
        online_free_lookup_email = f"""
        \33[1;49;93m[+] Searching for \33[1;49;96m{email}\33[1;49;93m on various platforms:
        \33[1;49;92m> Search engines:
        > https://www.google.com/search?q=%22{email}%22
        > https://www.bing.com/search?q=%22{email}%22
        > https://yandex.com/search/?text=%22{email}%22
        > Reliable sites:
        > https://thatsthem.com/email/{email}
        > https://www.ipqualityscore.com/free-email-validation-test/lookup/{email}
        > https://tools.emailhippo.com/email/inf/{email}
        > https://hunter.io/email-verifier/{email}
        > https://data.occrp.org/search?q={email}
        > https://www.truepeoplesearch.com/resultemail?email={email}
        > https://whoisology.com/email/{email}/1
        > https://scamsearch.io/search_report?searchoption=all&search={email}
        > Unreliable sites:
        > https://dehashed.com/search?query=%22{email}%22
        > https://portal.spycloud.com/endpoint/enriched-stats/{email}
        > https://cavalier.hudsonrock.com/api/json/v2/preview/search-by-login/osint-tools?email={email}
        > https://cleantalk.org/email-checker/{email}
        > https://spamdb.org/blacklists?q={email}
        > https://leakix.net/search?scope=leak&q=%22{email}%22
        > 
        \033[0m"""
        print(final_output)
        print(online_free_lookup_email)
    else:
        print("    > Invalid email address! (Example ******@gmail.com)")
        return False


# ?------------------------ email function ------------------------ #


# ?------------------------ check function ------------------------ #
# Check internet connection
def check_connection():
    # Checking internet connection
    urls = ["https://google.com", "https://bing.com"]
    try:
        requests.get(random.choice(urls), timeout=10)
        return True
    except:
        return False


# ?------------------------ check function ------------------------ #
# ?------------------------ number function ------------------------ #
# Reverse phone number lookup
def number_lookup(phone_number):
    # Importing modules
    from phonenumbers import timezone
    from phonenumbers import carrier
    from phonenumbers import geocoder

    # Global variables
    global prv_op
    prv_op = ""  # Resetting previous output

    # Information gathering about the number
    printit(
        f"    [+] Gathering information about \33[1;49;96m{phone_number}\33[1;49;93m...",
        coledt=[1, 49, 93],
        space_down=True,
    )
    prv_op += (
        f"\n    \33[1;49;93m[#] Reverse phone number lookup for \33[1;49;96m{phone_number}\33[1;49;93m:\033[0m"
        + "\n\n"
    )

    # Check if the number is valid or not (regex)
    if not re.match(r"^\+[1-9]\d{1,14}$", phone_number):
        printit("    > Invalid phone number format! (Example: +44xxxxxxxxxx) ", coledt=[1, 49, 91])
        return False
    # Country code check
    try:
        # Phone number format: (+Countrycode)xxxxxxxxxx
        phone_number_details = phonenumbers.parse(phone_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        printit("    > Missing Country Code! (Example: +91, +44, +1)", coledt=[1, 49, 91])
        return False
    # extract country_code & only_number from "Country Code: xx National Number: xxxxxxxxxx"
    country_code = (
        str(phone_number_details)
        .split("Country Code:", 1)[1]
        .split("National Number:", 1)[0]
        .strip()
    )
    only_number = (
        str(phone_number_details)
        .split("Country Code:", 1)[1]
        .split("National Number:", 1)[1]
        .strip()
    )

    # Validating a phone number
    valid = phonenumbers.is_valid_number(phone_number_details)

    # Checking possibility of a number
    possible = phonenumbers.is_possible_number(phone_number_details)

    if valid and possible:
        # Creating a phone number variable for country
        counrty_number = phonenumbers.parse(phone_number, "CH")

        # Gives mobile number's location (Region)
        region_code = phonenumbers.region_code_for_number(phone_number_details)

        # Gives mobile number's location (Country)
        country = geocoder.description_for_number(counrty_number, "en")

        # Creating a phone number variable for service provider
        service_number = phonenumbers.parse(phone_number, "RO")

        # Gives mobile number's service provider (Airtel, Idea, Jio)
        service_provider = carrier.name_for_number(service_number, "en")

        # Gives mobile number's timezone
        timezone_details_unfiltered = str(timezone.time_zones_for_number(phone_number_details))
        timezone_details = (
            timezone_details_unfiltered.replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace("(", "")
            .replace(")", "")
            .replace(",", "")
            .replace(" ", "")
        )

        # RFC3966 Format
        r_format = phonenumbers.format_number(
            phone_number_details, phonenumbers.PhoneNumberFormat.RFC3966
        ).replace("tel:", "")

        # Reconfiguring variables
        possible = str(possible) + " " * int(30 - len(str(possible)))
        valid = str(valid) + " " * int(30 - len(str(valid)))
        country_code = str(country_code) + " " * int(30 - len(str(country_code)))
        country = str(country) + " " * int(30 - len(str(country)))
        region_code = str(region_code) + " " * int(30 - len(str(region_code)))
        service_provider = str(service_provider) + " " * int(30 - len(str(service_provider)))
        timezone_details = str(timezone_details) + " " * int(30 - len(str(timezone_details)))
        phone_number = str(phone_number) + " " * int(30 - len(str(phone_number)))
        only_number = str(only_number) + " " * int(30 - len(str(only_number)))
        r_format = str(r_format) + " " * int(30 - len(str(r_format)))

        # Printing information
        final_output = f"""
    ┌──────────────────────────────────────────────────────┐
    | Scanned Phone Number: \33[1;49;96m{phone_number}\033[0m |
    |------------------------------------------------------|
    | INFORMATION         | DESCRIPTION                    |
    |------------------------------------------------------|
    | \33[1;49;97mPossible\033[0m            | {possible} |
    | \33[1;49;97mValid\033[0m               | {valid} |
    |------------------------------------------------------|
    | \33[1;49;97mCountry Code\033[0m        | {country_code} |
    | \33[1;49;97mCountry\033[0m             | {country} |
    | \33[1;49;97mRegion Code\033[0m         | {region_code} |
    | \33[1;49;97mService Provider\033[0m    | {service_provider} |
    | \33[1;49;97mTimezone\033[0m            | {timezone_details} |
    |------------------------------------------------------|
    | \33[1;49;97mInternational Format\033[0m| {phone_number} |
    | \33[1;49;97mNational Format\033[0m     | {only_number} |
    | \33[1;49;97mRFC3966 Format\033[0m      | {r_format} |
    └──────────────────────────────────────────────────────┘
        """
        print(final_output)
        prv_op += final_output + "\n"

        # Online free lookup services
        formatted_number = "-".join(
            [only_number.strip()[:3], only_number.strip()[3:6], only_number.strip()[6:]]
        )
        online_free_lookup_number = f"""
    \33[1;49;93m[+] Searching for \33[1;49;96m{phone_number.strip()}\33[1;49;93m on various platforms:

    \33[1;49;92m> Most Reliable: https://www.usphonebook.com/{formatted_number}
    > https://thatsthem.com/phone/{formatted_number}
    > https://www.ipqualityscore.com/reverse-phone-number-lookup/lookup/{region_code.strip()}/{only_number.strip()}
    > https://www.truecaller.com/search/{region_code.strip().lower()}/{only_number.strip()}
    > https://www.fastpeoplesearch.com/{formatted_number}
    > https://www.truepeoplesearch.com/resultphone?phoneno={only_number.strip()}

    \033[0m"""
        print(online_free_lookup_number)
        prv_op += online_free_lookup_number + "\n"

        # Google Dork Query to find more information about the number
        google_dork_queries = f"""
    \33[1;49;93m[+] Google Dork Queries:

    \33[1;49;92m> https://www.google.com/search?q={only_number.strip()}
    \033[0m"""
        print(google_dork_queries)
        prv_op += google_dork_queries + "\n"

        # Scanning social media platforms
        printit(f"    [+] Scanning social media platforms:", coledt=[1, 49, 93], space_down=True)

        return True
    else:
        # Reconfiguring variables
        possible = str(possible) + " " * int(30 - len(str(possible)))
        valid = str(valid) + " " * int(30 - len(str(valid)))
        phone_number = str(phone_number) + " " * int(30 - len(str(phone_number)))

        final_output = f"""
    ┌──────────────────────────────────────────────────────┐
    | Scanned Phone Number: \33[1;49;96m{phone_number}\033[0m |
    |------------------------------------------------------|
    | INFORMATION         | DESCRIPTION                    |
    |------------------------------------------------------|
    | \33[1;49;97mPossible\033[0m            | {possible} |
    | \33[1;49;97mValid\033[0m               | {valid} |
    └──────────────────────────────────────────────────────┘
        """
        print(final_output)
        prv_op += final_output + "\n"
        return False


# ?------------------------ number function ------------------------ #
# ?------------------------ ip function ------------------------ #
# Reverse ip address lookup
def ip_lookup(ip_address):
    # Global variables
    global prv_op
    prv_op = ""  # Resetting previous output

    # Checking internet connection
    printit(f"    [+] Verifying internet connection...", coledt=[1, 49, 93], space_down=True)
    if not check_connection():
        printit("    > Internet connection not available!", coledt=[1, 49, 91], space_down=True)
        return False
    # Information gathering about the ip address
    printit(
        f"    [+] Gathering information about \33[1;49;96m{ip_address}\33[1;49;93m...",
        coledt=[1, 49, 93],
        space_down=True,
    )
    prv_op += (
        f"    \33[1;49;93m[#] Reverse ip address lookup for \33[1;49;96m{ip_address}\33[1;49;93m:\033[0m"
        + "\n\n"
    )

    # Check if the ip address is valid or not (regex) [add IPv6 support]
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_address):
        printit("    > Invalid ip address format! (Example: 8.8.8.8)", coledt=[1, 49, 91])
        return False
    # IP address lookup APIs
    ip_addresses = [
        f"http://ip-api.com/json/{ip_address}",
        f"https://ipapi.co/{ip_address}/json/",
        f"http://ipwho.is/{ip_address}",
    ]
    ip_address = str(ip_address) + " " * int(30 - len(str(ip_address)))

    # Headers
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"}

    # Randomizing ip address lookup APIs
    random_api = random.choice([0, 1, 2])  # to not get rate limited

    # ip_addresses[0]
    if random_api == 0:
        try:
            # Getting response
            response = requests.get(ip_addresses[0], timeout=10, headers=headers)
            response_json = response.json()

            # Extracting data
            if response.status_code == 200 and response_json["status"] == "success":
                country = response_json["country"]
                countryCode = response_json["countryCode"]
                region = response_json["regionName"]
                regionCode = response_json["region"]
                city = response_json["city"]
                isp = response_json["isp"]
                org = response_json["org"]
                timezone = response_json["timezone"]
                postal = response_json["zip"]
                latitude = response_json["lat"]
                longitude = response_json["lon"]
                ip = response_json["query"]
            else:
                raise Exception("reverse-ip-lookup-server-1-error")
            # Reconfiguring variables
            country = str(country) + " " * int(30 - len(str(country)))
            countryCode = str(countryCode) + " " * int(30 - len(str(countryCode)))
            region = str(region) + " " * int(30 - len(str(region)))
            regionCode = str(regionCode) + " " * int(30 - len(str(regionCode)))
            city = str(city) + " " * int(30 - len(str(city)))
            isp = str(isp) + " " * int(30 - len(str(isp)))
            org = str(org) + " " * int(30 - len(str(org)))
            timezone = str(timezone) + " " * int(30 - len(str(timezone)))
            postal = str(postal) + " " * int(30 - len(str(postal)))
            latitude = str(latitude) + " " * int(30 - len(str(latitude)))
            longitude = str(longitude) + " " * int(30 - len(str(longitude)))
            ip = str(ip) + " " * int(30 - len(str(ip)))

            # Printing information
            final_output = f"""
    ┌──────────────────────────────────────────────────────┐
    | Scanned IP Address: \33[1;49;96m{ip_address}\033[0m   |
    |------------------------------------------------------|
    | INFORMATION         | DESCRIPTION                    |
    |------------------------------------------------------|
    | \33[1;49;97mCountry\033[0m             | {country} |
    | \33[1;49;97mCountry Code\033[0m        | {countryCode} |
    | \33[1;49;97mRegion\033[0m              | {region} |
    | \33[1;49;97mRegion Code\033[0m         | {regionCode} |
    | \33[1;49;97mCity\033[0m                | {city} |
    |------------------------------------------------------|
    | \33[1;49;97mPostal Code\033[0m         | {postal} |
    | \33[1;49;97mTimezone\033[0m            | {timezone} |
    | \33[1;49;97mLatitude\033[0m            | {latitude} |
    | \33[1;49;97mLongitude\033[0m           | {longitude} |
    |------------------------------------------------------|
    | \33[1;49;97mISP\033[0m                 | {isp} |
    | \33[1;49;97mOrg\033[0m                 | {org} |
    └──────────────────────────────────────────────────────┘
    """
            print(final_output)
            online_free_lookup_ip = f"""
        \33[1;49;93m[+] Searching for \33[1;49;96m{ip_address}\33[1;49;93m on various platforms:

        \33[1;49;92m> Reliable sites:
        > https://thatsthem.com/ip/{ip_address}
        > https://www.ipaddress.com/ipv4/{ip_address}
        > https://dnschecker.org/ip-whois-lookup.php?query={ip_address}
        > https://www.ip-lookup.org/location/{ip_address}
        > https://www.iplocation.net/ip-lookup?query={ip_address}
        > https://www.shodan.io/host/{ip_address}
        > https://beta.shodan.io/host/{ip_address}
        > https://search.censys.io/hosts/{ip_address}
        > https://leakix.net/host/{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=arin%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blocklist%3a{ip_address}
        > Unreliable sites:
        > https://viewdns.info/iplocation/?ip={ip_address}
        > https://viewdns.info/whois/?domain={ip_address}
        > https://viewdns.info/traceroute/?ip={ip_address}
        > https://viewdns.info/reverseip/?host={ip_address}&t=1
        > https://www.bing.com/search?q=ip%3A{ip_address}

        \033[0m"""
            print(online_free_lookup_ip)
            prv_op += online_free_lookup_ip + "\n"
        except Exception as e:
            print(e)
            final_output = f"""
    ┌──────────────────────────────────────────────────────┐
    | Scanned IP Address: \33[1;49;96m{ip_address}\033[0m   |
    |------------------------------------------------------|
    | \33[1;49;91mFailed to Fetch information from this server!\033[0m        |
    └──────────────────────────────────────────────────────┘
    """
            print(final_output)
            online_free_lookup_ip = f"""
        \33[1;49;93m[+] Searching for \33[1;49;96m{ip_address}\33[1;49;93m on various platforms:

        \33[1;49;92m> Reliable sites:
        > https://thatsthem.com/ip/{ip_address}
        > https://www.ipaddress.com/ipv4/{ip_address}
        > https://dnschecker.org/ip-whois-lookup.php?query={ip_address}
        > https://www.ip-lookup.org/location/{ip_address}
        > https://www.iplocation.net/ip-lookup?query={ip_address}
        > https://www.shodan.io/host/{ip_address}
        > https://beta.shodan.io/host/{ip_address}
        > https://search.censys.io/hosts/{ip_address}
        > https://leakix.net/host/{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=arin%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blocklist%3a{ip_address}
        > Unreliable sites:
        > https://viewdns.info/iplocation/?ip={ip_address}
        > https://viewdns.info/whois/?domain={ip_address}
        > https://viewdns.info/traceroute/?ip={ip_address}
        > https://viewdns.info/reverseip/?host={ip_address}
        > https://www.bing.com/search?q=ip%3A{ip_address}

        \033[0m"""
            print(online_free_lookup_ip)
            prv_op += online_free_lookup_ip + "\n"
    # ip_addresses[1]
    elif random_api == 1:
        try:
            # Getting response_json
            response = requests.get(ip_addresses[1], timeout=10, headers=headers)
            response_json = response.json()

            # Extracting data
            if response.status_code == 200:
                ip = response_json["ip"]
                network = response_json["network"]
                version = response_json["version"]
                city = response_json["city"]
                region = response_json["region"]
                region_code = response_json["region_code"]
                country = response_json["country_name"]
                country_name = response_json["country_name"]
                country_code = response_json["country_code"]
                country_code_iso3 = response_json["country_code_iso3"]
                country_capital = response_json["country_capital"]
                country_tld = response_json["country_tld"]
                continent_code = response_json["continent_code"]
                in_eu = response_json["in_eu"]
                postal = response_json["postal"]
                latitude = response_json["latitude"]
                longitude = response_json["longitude"]
                timezone = response_json["timezone"]
                utc_offset = response_json["utc_offset"]
                country_calling_code = response_json["country_calling_code"]
                currency = response_json["currency"]
                currency_name = response_json["currency_name"]
                languages = response_json["languages"]
                country_area = response_json["country_area"]
                country_population = response_json["country_population"]
                asn = response_json["asn"]
                org = response_json["org"]
            else:
                raise Exception("reverse-ip-lookup-server-2-error")
            # Reconfiguring variables
            ip = str(ip) + " " * int(30 - len(str(ip)))
            network = str(network) + " " * int(30 - len(str(network)))
            version = str(version) + " " * int(30 - len(str(version)))
            city = str(city) + " " * int(30 - len(str(city)))
            region = str(region) + " " * int(30 - len(str(region)))
            region_code = str(region_code) + " " * int(30 - len(str(region_code)))
            country = str(country) + " " * int(30 - len(str(country)))
            country_name = str(country_name) + " " * int(30 - len(str(country_name)))
            country_code = str(country_code) + " " * int(30 - len(str(country_code)))
            country_code_iso3 = str(country_code_iso3) + " " * int(30 - len(str(country_code_iso3)))
            country_capital = str(country_capital) + " " * int(30 - len(str(country_capital)))
            country_tld = str(country_tld) + " " * int(30 - len(str(country_tld)))
            continent_code = str(continent_code) + " " * int(30 - len(str(continent_code)))
            in_eu = str(in_eu) + " " * int(30 - len(str(in_eu)))
            postal = str(postal) + " " * int(30 - len(str(postal)))
            latitude = str(latitude) + " " * int(30 - len(str(latitude)))
            longitude = str(longitude) + " " * int(30 - len(str(longitude)))
            timezone = str(timezone) + " " * int(30 - len(str(timezone)))
            utc_offset = str(utc_offset) + " " * int(30 - len(str(utc_offset)))
            country_calling_code = str(country_calling_code) + " " * int(
                30 - len(str(country_calling_code))
            )
            currency = str(currency) + " " * int(30 - len(str(currency)))
            currency_name = str(currency_name) + " " * int(30 - len(str(currency_name)))
            languages = str(languages) + " " * int(30 - len(str(languages)))
            country_area = str(country_area) + " " * int(30 - len(str(country_area)))
            country_population = str(country_population) + " " * int(
                30 - len(str(country_population))
            )
            asn = str(asn) + " " * int(30 - len(str(asn)))
            org = str(org) + " " * int(30 - len(str(org)))

            # Printing information
            final_output = f"""
    ┌──────────────────────────────────────────────────────┐
    | Scanned IP Address: \33[1;49;96m{ip_address}\033[0m   |
    |------------------------------------------------------|
    | INFORMATION         | DESCRIPTION                    |
    |------------------------------------------------------|
    | \33[1;49;97mIP Type\033[0m             | {version} |
    | \33[1;49;97mNetwork\033[0m             | {network} |
    |------------------------------------------------------|
    | \33[1;49;97mCountry\033[0m             | {country} |
    | \33[1;49;97mCountry Name\033[0m        | {country_name} |
    | \33[1;49;97mCountry Code\033[0m        | {country_code} |
    | \33[1;49;97mCountry Code ISO3\033[0m   | {country_code_iso3} |
    | \33[1;49;97mCountry Capital\033[0m     | {country_capital} |
    | \33[1;49;97mRegion\033[0m              | {region} |
    | \33[1;49;97mRegion Code\033[0m         | {region_code} |
    | \33[1;49;97mCity\033[0m                | {city} |
    |------------------------------------------------------|
    | \33[1;49;97mCountry TLD\033[0m         | {country_tld} |
    | \33[1;49;97mCalling Prefix\033[0m      | {country_calling_code} |
    | \33[1;49;97mContinent Code\033[0m      | {continent_code} |
    | \33[1;49;97mIn EU\033[0m               | {in_eu} |
    | \33[1;49;97mApprox. Area\033[0m        | {country_area} |
    | \33[1;49;97mApprox. Population\033[0m  | {country_population} |
    | \33[1;49;97mLanguages Spoken\033[0m    | {languages} |
    | \33[1;49;97mCurrency\033[0m            | {currency} |
    | \33[1;49;97mCurrency Name\033[0m       | {currency_name} |
    |------------------------------------------------------|
    | \33[1;49;97mPostal Code\033[0m         | {postal} |
    | \33[1;49;97mLatitude\033[0m            | {latitude} |
    | \33[1;49;97mLongitude\033[0m           | {longitude} |
    | \33[1;49;97mTimezone\033[0m            | {timezone} |
    | \33[1;49;97mUTC Offset\033[0m          | {utc_offset} |
    |------------------------------------------------------|
    | \33[1;49;97mASN\033[0m                 | {asn} |
    | \33[1;49;97mISP\033[0m                 | {org} |
    └──────────────────────────────────────────────────────┘
    """
            print(final_output)
            online_free_lookup_ip = f"""
        \33[1;49;93m[+] Searching for \33[1;49;96m{ip_address}\33[1;49;93m on various platforms:

        \33[1;49;92m> Reliable sites:
        > https://thatsthem.com/ip/{ip_address}
        > https://www.ipaddress.com/ipv4/{ip_address}
        > https://dnschecker.org/ip-whois-lookup.php?query={ip_address}
        > https://www.ip-lookup.org/location/{ip_address}
        > https://www.iplocation.net/ip-lookup?query={ip_address}
        > https://www.shodan.io/host/{ip_address}
        > https://beta.shodan.io/host/{ip_address}
        > https://search.censys.io/hosts/{ip_address}
        > https://leakix.net/host/{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=arin%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blocklist%3a{ip_address}
        > Unreliable sites:
        > https://viewdns.info/iplocation/?ip={ip_address}
        > https://viewdns.info/whois/?domain={ip_address}
        > https://viewdns.info/traceroute/?ip={ip_address}
        > https://viewdns.info/reverseip/?host={ip_address}
        > https://www.bing.com/search?q=ip%3A{ip_address}

        \033[0m"""
            print(online_free_lookup_ip)
            prv_op += online_free_lookup_ip + "\n"
        except:
            final_output = f"""
    ┌──────────────────────────────────────────────────────┐
    | Scanned IP Address: \33[1;49;96m{ip_address}\033[0m   |
    |------------------------------------------------------|
    | \33[1;49;91mFailed to Fetch information from this server!\033[0m        |
    └──────────────────────────────────────────────────────┘
    """
            print(final_output)
            online_free_lookup_ip = f"""
        \33[1;49;93m[+] Searching for \33[1;49;96m{ip_address}\33[1;49;93m on various platforms:

        \33[1;49;92m> Reliable sites:
        > https://thatsthem.com/ip/{ip_address}
        > https://www.ipaddress.com/ipv4/{ip_address}
        > https://dnschecker.org/ip-whois-lookup.php?query={ip_address}
        > https://www.ip-lookup.org/location/{ip_address}
        > https://www.iplocation.net/ip-lookup?query={ip_address}
        > https://www.shodan.io/host/{ip_address}
        > https://beta.shodan.io/host/{ip_address}
        > https://search.censys.io/hosts/{ip_address}
        > https://leakix.net/host/{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=arin%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blocklist%3a{ip_address}
        > Unreliable sites:
        > https://viewdns.info/iplocation/?ip={ip_address}
        > https://viewdns.info/whois/?domain={ip_address}
        > https://viewdns.info/traceroute/?ip={ip_address}
        > https://viewdns.info/reverseip/?host={ip_address}
        > https://www.bing.com/search?q=ip%3A{ip_address}

        \033[0m"""
            print(online_free_lookup_ip)
            prv_op += online_free_lookup_ip + "\n"
    # ip_addresses[2]
    elif random_api == 2:
        try:
            # Getting response_json
            response = requests.get(ip_addresses[2], timeout=10, headers=headers)
            response_json = response.json()

            # Extracting data
            if response.status_code == 200 and response_json["success"] == True:
                ip = response_json["ip"]
                ip_type = response_json["type"]
                continent = response_json["continent"]
                continent_code = response_json["continent_code"]
                country = response_json["country"]
                country_code = response_json["country_code"]
                region = response_json["region"]
                region_code = response_json["region_code"]
                city = response_json["city"]
                latitude = response_json["latitude"]
                longitude = response_json["longitude"]
                is_eu = response_json["is_eu"]
                postal = response_json["postal"]
                calling_code = response_json["calling_code"]
                capital = response_json["capital"]
                borders = response_json["borders"]
                flag_img = response_json["flag"]["img"]
                flag_emoji = response_json["flag"]["emoji"]
                flag_emoji_unicode = response_json["flag"]["emoji_unicode"]
                asn = response_json["connection"]["asn"]
                org = response_json["connection"]["org"]
                isp = response_json["connection"]["isp"]
                domain = response_json["connection"]["domain"]
                timezone_id = response_json["timezone"]["id"]
                timezone_abbr = response_json["timezone"]["abbr"]
                timezone_is_dst = response_json["timezone"]["is_dst"]
                timezone_offset = response_json["timezone"]["offset"]
                timezone_utc = response_json["timezone"]["utc"]
                timezone_current_time = response_json["timezone"]["current_time"]
            else:
                raise Exception("reverse-ip-lookup-server-3-error")
            # Reconfiguring variables
            ip = str(ip) + " " * int(30 - len(str(ip)))
            ip_type = str(ip_type) + " " * int(30 - len(str(ip_type)))
            continent = str(continent) + " " * int(30 - len(str(continent)))
            continent_code = str(continent_code) + " " * int(30 - len(str(continent_code)))
            country = str(country) + " " * int(30 - len(str(country)))
            country_code = str(country_code) + " " * int(30 - len(str(country_code)))
            region = str(region) + " " * int(30 - len(str(region)))
            region_code = str(region_code) + " " * int(30 - len(str(region_code)))
            city = str(city) + " " * int(30 - len(str(city)))
            latitude = str(latitude) + " " * int(30 - len(str(latitude)))
            longitude = str(longitude) + " " * int(30 - len(str(longitude)))
            is_eu = str(is_eu) + " " * int(30 - len(str(is_eu)))
            postal = str(postal) + " " * int(30 - len(str(postal)))
            calling_code = str(calling_code) + " " * int(30 - len(str(calling_code)))
            capital = str(capital) + " " * int(30 - len(str(capital)))
            borders = str(borders) + " " * int(30 - len(str(borders)))
            flag_img = str(flag_img) + " " * int(30 - len(str(flag_img)))
            flag_emoji = str(flag_emoji) + " " * int(30 - len(str(flag_emoji)))
            flag_emoji_unicode = str(flag_emoji_unicode) + " " * int(
                30 - len(str(flag_emoji_unicode))
            )
            asn = str(asn) + " " * int(30 - len(str(asn)))
            org = str(org) + " " * int(30 - len(str(org)))
            isp = str(isp) + " " * int(30 - len(str(isp)))
            domain = str(domain) + " " * int(30 - len(str(domain)))
            timezone_id = str(timezone_id) + " " * int(30 - len(str(timezone_id)))
            timezone_abbr = str(timezone_abbr) + " " * int(30 - len(str(timezone_abbr)))
            timezone_is_dst = str(timezone_is_dst) + " " * int(30 - len(str(timezone_is_dst)))
            timezone_offset = str(timezone_offset) + " " * int(30 - len(str(timezone_offset)))
            timezone_utc = str(timezone_utc) + " " * int(30 - len(str(timezone_utc)))
            timezone_current_time = str(timezone_current_time) + " " * int(
                30 - len(str(timezone_current_time))
            )

            # Printing information
            final_output = f"""
    ┌──────────────────────────────────────────────────────┐
    | Scanned IP Address: \33[1;49;96m{ip_address}\033[0m   |
    |------------------------------------------------------|
    | INFORMATION         | DESCRIPTION                    |
    |------------------------------------------------------|
    | \33[1;49;97mIP Type\033[0m             | {ip_type} |
    |------------------------------------------------------|
    | \33[1;49;97mCountry\033[0m             | {country} |
    | \33[1;49;97mCountry Code\033[0m        | {country_code} |
    | \33[1;49;97mRegion\033[0m              | {region} |
    | \33[1;49;97mRegion Code\033[0m         | {region_code} |
    | \33[1;49;97mCity\033[0m                | {city} |
    |------------------------------------------------------|
    | \33[1;49;97mCountry Capital\033[0m     | {capital} |
    | \33[1;49;97mContinent\033[0m           | {continent} |
    | \33[1;49;97mContinent Code\033[0m      | {continent_code} |
    | \33[1;49;97mIn EU\033[0m               | {is_eu} |
    | \33[1;49;97mSharing Border with\033[0m | {borders} |
    | \33[1;49;97mFlag Emoji\033[0m          | {flag_emoji_unicode} |
    |------------------------------------------------------|
    | \33[1;49;97mPostal Code\033[0m         | {postal} |
    | \33[1;49;97mCalling Prefix\033[0m      | {calling_code} |
    | \33[1;49;97mLatitude\033[0m            | {latitude} |
    | \33[1;49;97mLongitude\033[0m           | {longitude} |
    |------------------------------------------------------|
    | \33[1;49;97mTimezone\033[0m            | {timezone_id} |
    | \33[1;49;97mTimezone Abbr\033[0m       | {timezone_abbr} |
    | \33[1;49;97mTimezone is DST\033[0m     | {timezone_is_dst} |
    | \33[1;49;97mTimezone Offset\033[0m     | {timezone_offset} |
    | \33[1;49;97mTimezone UTC\033[0m        | {timezone_utc} |
    | \33[1;49;97mCurrent Time\033[0m        | {timezone_current_time} |
    |------------------------------------------------------|
    | \33[1;49;97mASN\033[0m                 | {asn} |
    | \33[1;49;97mISP\033[0m                 | {isp} |
    | \33[1;49;97mDomain\033[0m              | {domain} |
    └──────────────────────────────────────────────────────┘
    """
            print(final_output)
            online_free_lookup_ip = f"""
        \33[1;49;93m[+] Searching for \33[1;49;96m{ip_address}\33[1;49;93m on various platforms:

        \33[1;49;92m> Reliable sites:
        > https://thatsthem.com/ip/{ip_address}
        > https://www.ipaddress.com/ipv4/{ip_address}
        > https://dnschecker.org/ip-whois-lookup.php?query={ip_address}
        > https://www.ip-lookup.org/location/{ip_address}
        > https://www.iplocation.net/ip-lookup?query={ip_address}
        > https://www.shodan.io/host/{ip_address}
        > https://beta.shodan.io/host/{ip_address}
        > https://search.censys.io/hosts/{ip_address}
        > https://leakix.net/host/{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=arin%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blocklist%3a{ip_address}
        > Unreliable sites:
        > https://viewdns.info/iplocation/?ip={ip_address}
        > https://viewdns.info/whois/?domain={ip_address}
        > https://viewdns.info/traceroute/?ip={ip_address}
        > https://viewdns.info/reverseip/?host={ip_address}
        > https://www.bing.com/search?q=ip%3A{ip_address}

        \033[0m"""
            print(online_free_lookup_ip)
            prv_op += online_free_lookup_ip + "\n"
        except:
            final_output = f"""
    ┌──────────────────────────────────────────────────────┐
    | Scanned IP Address: \33[1;49;96m{ip_address}\033[0m   |
    |------------------------------------------------------|
    | \33[1;49;91mFailed to Fetch information from this server!\033[0m        |
    └──────────────────────────────────────────────────────┘
    """
            print(final_output)
            online_free_lookup_ip = f"""
        \33[1;49;93m[+] Searching for \33[1;49;96m{ip_address}\33[1;49;93m on various platforms:

        \33[1;49;92m> Reliable sites:
        > https://thatsthem.com/ip/{ip_address}
        > https://www.ipaddress.com/ipv4/{ip_address}
        > https://dnschecker.org/ip-whois-lookup.php?query={ip_address}
        > https://www.ip-lookup.org/location/{ip_address}
        > https://www.iplocation.net/ip-lookup?query={ip_address}
        > https://www.shodan.io/host/{ip_address}
        > https://beta.shodan.io/host/{ip_address}
        > https://search.censys.io/hosts/{ip_address}
        > https://leakix.net/host/{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=arin%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a{ip_address}
        > https://mxtoolbox.com/SuperTool.aspx?action=blocklist%3a{ip_address}
        > Unreliable sites:
        > https://viewdns.info/iplocation/?ip={ip_address}
        > https://viewdns.info/whois/?domain={ip_address}
        > https://viewdns.info/traceroute/?ip={ip_address}
        > https://viewdns.info/reverseip/?host={ip_address}
        > https://www.bing.com/search?q=ip%3A{ip_address}

        \033[0m"""
            print(online_free_lookup_ip)
            prv_op += online_free_lookup_ip + "\n"
    return True


# ?------------------------ ip function ------------------------ #
# ?------------------------ mac function ------------------------ #
# Reverse mac address lookup
def mac_lookup(mac_address):
    # https://api.macvendors.com/<mac_address>

    # Global variables
    global prv_op
    prv_op = ""  # Resetting previous output

    # Information gathering about the mac address
    printit(
        f"    [+] Gathering information about \33[1;49;96m{mac_address}\33[1;49;93m...",
        coledt=[1, 49, 93],
        space_down=True,
    )
    prv_op += (
        f"    \33[1;49;93m[#] Reverse mac address lookup for \33[1;49;96m{mac_address}\33[1;49;93m:\033[0m"
        + "\n\n"
    )

    # Check if the mac address is valid or not (regex)
    if not re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac_address):
        printit(
            "    > Invalid mac address format! (Example: 00:00:00:00:00:00)", coledt=[1, 49, 91]
        )
        return False
    # Getting mac address vendor
    try:
        vendor = MacLookup().lookup(mac_address)
        bol_val = True
    except KeyError:
        vendor = "\33[1;49;91mNot Found\033[0m"
        bol_val = False
    # Reconfiguring variables
    mac_address = str(mac_address) + " " * int(31 - len(str(mac_address)))
    vendor = str(vendor) + " " * int((36 + 14) - len(str(vendor)))

    # Printing information
    final_output = f"""
    ┌──────────────────────────────────────────────────────┐
    | Scanned MAC Address: \33[1;49;96m{mac_address}\033[0m |
    |------------------------------------------------------|
    | INFORMATION   | DESCRIPTION                          |
    |------------------------------------------------------|
    | \33[1;49;97mVendor\033[0m        | {vendor} |
    └──────────────────────────────────────────────────────┘
    """
    print(final_output)
    prv_op += final_output + "\n"

    return bol_val


# ?------------------------ mac function ------------------------ #
# ?------------------------ whosis function ------------------------ #
# Reverse whois lookup
def whois_lookup(domain):
    # Global variables
    global prv_op
    prv_op = ""  # Resetting previous output

    # Checking internet connection
    printit(f"    [+] Verifying internet connection...", coledt=[1, 49, 93], space_down=True)
    if not check_connection():
        printit("    > Internet connection not available!", coledt=[1, 49, 91], space_down=True)
        return False
    # Information gathering about the domain
    printit(
        f"    [+] Gathering information about \33[1;49;96m{domain}\33[1;49;93m...",
        coledt=[1, 49, 93],
        space_down=True,
    )
    prv_op += (
        f"    \33[1;49;93m[#] Reverse whois lookup for \33[1;49;96m{domain}\33[1;49;93m:\033[0m"
        + "\n\n"
    )

    # Domain validation (regex)
    if not re.match(r"^([a-zA-Z0-9]+(-[a-zA-Z0-9]+)*\.)+[a-zA-Z]{2,}$", domain):
        printit("    > Invalid domain format! (Example: example.com)", coledt=[1, 49, 91])
        return False
    # Getting whois information
    try:
        whois_info = whois.whois(domain)
        bol_val = True
    except:
        bol_val = False
    # Reconfiguring variables
    domain = str(domain) + " " * int(36 - len(str(domain)))

    # Printing information
    final_output = f"""
    ┌──────────────────────────────────────────────────────┐
    | Scanned Domain: \33[1;49;96m{domain}\033[0m |
    |------------------------------------------------------|
    | INFORMATION   | DESCRIPTION                          |
    |------------------------------------------------------|"""

    # If whois information is available
    if bol_val:
        # Loop through whois information & add it to the final output
        for key, value in whois_info.items():
            # Filtering out some keys
            if key == "status":
                continue
            if key == "expiration_date":
                key = "expiry_date"
            if key == "registrant_postal_code":
                key = "postal_code"

            # Reconfiguring variables
            key = key.replace("_", " ").capitalize()

            # Adding formatted information to the final output
            if type(value) == list:
                key = str(key) + " " * int(13 - len(str(key)))
                value_1 = str(value[0]) + " " * int(36 - len(str(value[0])))
                final_output += f"""\n    | \33[1;49;97m{key}\033[0m | {value_1} |"""
                if len(value) > 1:
                    for i in range(1, len(value)):
                        value_2 = str(value[i]) + " " * int(36 - len(str(value[i])))
                        final_output += f"""\n    |               | {value_2} |"""
            else:
                key = str(key) + " " * int(13 - len(str(key)))
                value = str(value) + " " * int(36 - len(str(value)))
                final_output += f"""\n    | \33[1;49;97m{key}\033[0m | {value} |"""
    else:
        final_output += f"""\n    | \33[1;49;97mInformation\033[0m   | \33[1;49;91mNot Found\033[0m{' '*int(36-len('Not Found'))} |"""
    # Add the last part of the final output
    final_output += f"""\n    └──────────────────────────────────────────────────────┘"""
    printit(
        f"    [+] Loading for \33[1;49;96m{domain}\33[1;49;93m.",
        coledt=[1, 49, 93],
        space_down=True,
    )
    time.sleep(1)
    printit(
        f"    [+] Loading for \33[1;49;96m{domain}\33[1;49;93m..",
        coledt=[1, 49, 93],
        space_down=True,
    )
    time.sleep(1)
    printit(
        f"    [+] Loading for \33[1;49;96m{domain}\33[1;49;93m...",
        coledt=[1, 49, 93],
        space_down=True,
    )
    time.sleep(1)
    print(final_output)
    online_free_lookup_whois = f"""
\33[1;49;93m[+] Searching for \33[1;49;96m{domain}\33[1;49;93m on various platforms:

\33[1;49;92m> Most Reliable: https://sitereport.netcraft.com/?url={domain}
> https://www.shodan.io/search?query={domain}
> https://search.censys.io/search?resource=hosts&sort=RELEVANCE&per_page=25&virtual_hosts=EXCLUDE&q={domain}
> https://securityheaders.com/?q={domain}
> https://www.zoomeye.org/searchResult?q=site:{domain}


\033[0m"""

    print(online_free_lookup_whois)
    prv_op += online_free_lookup_whois + "\n"

    return bol_val


# ?------------------------ whois function ------------------------ #
# ?------------------------ dns function ------------------------ #
# Reverse domain lookup
def dns_lookup(ip_or_domain):
    # Global variables
    global prv_op
    prv_op = ""  # Resetting previous output

    # Checking internet connection
    printit(f"    [+] Verifying internet connection...", coledt=[1, 49, 93], space_down=True)
    if not check_connection():
        printit("    > Internet connection not available!", coledt=[1, 49, 91], space_down=True)
        return False
    # Information gathering about the domain
    printit(
        f"    [+] Gathering information about \33[1;49;96m{ip_or_domain}\33[1;49;93m...",
        coledt=[1, 49, 93],
        space_down=True,
    )

    # Validating ip address or domain name (regex)
    if re.match(r"^([a-zA-Z0-9]+(-[a-zA-Z0-9]+)*\.)+[a-zA-Z]{2,}$", ip_or_domain):
        prv_op += (
            f"    \33[1;49;93m[#] DNS lookup for \33[1;49;96m{ip_or_domain}\33[1;49;93m:\033[0m"
            + "\n\n"
        )
        domain = ip_or_domain + " " * int(36 - len(ip_or_domain))
        final_output_scanned = f"    | Scanned Domain: \33[1;49;96m{domain}\033[0m |"
        try:
            ip = socket.gethostbyname(ip_or_domain)
            ip = str(ip) + " " * int(36 - len(str(ip)))
        except:
            ip = "\33[1;49;91mNot Found\033[0m" + " " * int(36 - len("Not Found"))
    elif re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}$", ip_or_domain):
        prv_op += (
            f"    \33[1;49;93m[#] Reverse DNS lookup for \33[1;49;96m{ip_or_domain}\33[1;49;93m:\033[0m"
            + "\n\n"
        )
        ip = ip_or_domain + " " * int(36 - len(ip_or_domain))
        final_output_scanned = f"    | Scanned IP: \33[1;49;96m{ip}\033[0m     |"
        try:
            domain = socket.gethostbyaddr(ip_or_domain)[0]
            domain = str(domain) + " " * int(36 - len(str(domain)))
        except:
            domain = "\33[1;49;91mNot Found\033[0m" + " " * int(36 - len("Not Found"))
    else:
        printit("    > Invalid ip address or domain name!", coledt=[1, 49, 91], space_down=True)
        return False
    # Expcepts: socket.gaierror, socket.herror

    # Printing information
    final_output_remaining = f"""
    |------------------------------------------------------|
    | INFORMATION   | DESCRIPTION                          |
    |------------------------------------------------------|
    | \33[1;49;97mIP\033[0m            | {ip} |
    | \33[1;49;97mDomain\033[0m        | {domain} |
    └──────────────────────────────────────────────────────┘
    """

    print(
        "\n    ┌──────────────────────────────────────────────────────┐\n"
        + final_output_scanned
        + final_output_remaining
    )
    prv_op += (
        "\n    ┌──────────────────────────────────────────────────────┐"
        + "\n"
        + final_output_scanned
        + final_output_remaining
    )

    return True


# ?------------------------ dns function ------------------------ #
# --------------------------- Basic functions ------------------------ #
# ?------------------------ search website function (Not in help)------------------------ #
def search_websites(websites):
    for website in websites:
        print(f"Searching: {website} ", end="", flush=True)
        loading_time = random.uniform(
            1, 5
        )  # Generate a random loading time between 3 and 10 seconds
        for _ in range(20):  # Simulate a loading bar with 20 steps
            time.sleep(loading_time / 20)  # Adjust the sleep duration based on loading time
            print(".", end="", flush=True)
        print("Done")
        time.sleep(0.5)


websites_to_search = ["Website1", "Website2", "Website3"]  # Replace with your list of websites

# ?------------------------ search website function (Not in help)------------------------ #


# ?------------------------ loading function (Not in help)------------------------ #
def loading(loading_list):
    for loading_task in loading_list:
        formatted_loading_task = (
            f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}{loading_task}{Style.RESET_ALL}"
        )
        print(f"Loading Task: {formatted_loading_task} ", end="", flush=True)
        loading_time = random.uniform(0.01, 0.1)
        for _ in range(20):
            time.sleep(loading_time / 20)
            print(".", end="", flush=True)
        print(" Done")
        time.sleep(0.05)


loading_list = [
    "Loading Command: help",
    "Loading Command: exit/quit",
    "Loading Command: Google Dorks",
    "Loading Command: Reverse Image Lookup",
    "Loading Command: Internet Connection Checker",
    "Loading Command: Clear",
    "Loading Command: Save",
    "Loading Command: Info",
    "Loading Command: User Input Color",
    "Loading Scanner: Reverse Phone Number Lookup",
    "Loading Scanner: Reverse Email Address Lookup",
    "Loading Scanner: Reverse IP Address Lookup",
    "Loading Scanner: Reverse Whois Lookup",
    "Loading Scanner: Reverse MAC Address Lookup",
    "Loading Scanner: Reverse DNS Lookup",
    "Loading Scanner: Reverse Name Lookup",
    "Loading Scanner: Reverse Coordinate"
]
# ?------------------------ loading function (Not in help)------------------------ #


# ?------------------------ printit function (Not in help)------------------------ #
def printit(
    text,
    center="",
    line_up=False,
    line_down=False,
    space_up=False,
    space_down=False,
    coledt=[0, 0, 0],
    normaltxt_start="",
    normaltxt_end="",
    hide=False,
    verbose_mode=False,
    input_mode=False,
):
    if not hide or verbose_mode:
        # get terminal width
        width = os.get_terminal_size().columns

        # printing text
        if space_up:
            print()
        if line_up:
            print("⸺" * width)

        print(normaltxt_start, end="")

        new_width = int((width - len(text)) / 2)
        print(center * new_width, end="")
        print(f"\33[{coledt[0]};{coledt[1]};{coledt[2]}m", end="")
        if input_mode:
            input_var = input(text)
        else:
            print(str(text), end="")
        print("\033[0m", end="")
        print(center * new_width)

        print(normaltxt_end, end="")

        if line_down:
            print("⸺" * width)
        if space_down:
            print()

        if input_mode:
            return input_var


# ?------------------------ printit function (Not in help)------------------------ #
# ?------------------------ save function (Not in help)------------------------ #
def save_output(prv_cmd):
    try:
        filename = prv_cmd + "_Work in progess_" + str(time.strftime("%d-%m-%Y_%H-%M-%S")) + ".txt"
        pwd = os.getcwd()
        os_name = os.uname()
        path = pwd + "/" + filename

        file_save_info = f"""
    \33[1;49;93m[#] Output File Name: \33[1;49;97m{filename}\033[0m
    \33[1;49;93m[#] Output File Path: \33[1;49;97m{path}\033[0m
        """
        print(file_save_info)

        header = f"""
    \33[1;49;93m[@] Osint framework: \33[1;49;96mIf ur seeing this then
    \33[1;49;93m[@] Github: \33[1;49;96mNo rizz?

    \33[1;49;93m[#] Output File Name: \33[1;49;97m{filename}
    \33[1;49;93m[#] Output File Path: \33[1;49;97m{path}
    \33[1;49;93m[#] Date: \33[1;49;97m{str(time.strftime("%d-%m-%Y"))}
    \33[1;49;93m[#] Time: \33[1;49;97m{str(time.strftime("%H:%M:%S"))}

    \33[1;49;93m[#] Command Executed: \33[1;49;96m{full_cmd.strip()}\n"""

        with open(path, "w") as f:
            f.write(header)
            f.write(prv_op)
        printit(
            f"    [+] Excute following commands to view output:",
            coledt=[1, 49, 93],
            space_down=True,
            space_up=True,
        )

        if os_name == "nt":
            exe_cmd = f"""    \33[1;49;93m> \33[1;49;92mshell more {filename}\033[0m
    \33[1;49;93m> \33[1;49;92mshell type {filename}\033[0m"""
        else:
            exe_cmd = f"""    \33[1;49;93m> \33[1;49;92mshell cat {filename}\033[0m
    \33[1;49;93m> \33[1;49;92mshell less {filename}\033[0m"""
        print(exe_cmd)

        return True
    except:
        printit(f"    [!] Output could not be saved!", coledt=[1, 49, 91], space_down=True)
        return False


# ?------------------------ save function (Not in help)------------------------ #
# ?------------------------ dork function ------------------------ #
def dork_query():
    # Dork query from exploit-db
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
        }
        dork_query = requests.get(
            "https://www.exploit-db.com/ghdb/" + str(random.randint(1000, 8000)), headers=headers
        )

        # If exploit-db is available
        if dork_query.status_code == 200:
            # Parsing html
            parsed_html = bs4.BeautifulSoup(dork_query.text, "html.parser")

            # extracting query (h1 -> class: card-title)
            query = parsed_html.find("h1", attrs={"class": "card-title"}).text.strip()

            return query
    except:
        pass
    # If dork query is not available, use local dork query
    local_dork_query = [
        "site:domain.com filetype: pdf",
        "inurl: password",
        "intext:”username”",
        "filetype:xls",
        "filetype:txt “username”",
        "filetype:log “PHP Parse error” | “PHP Warning” | “PHP Error”",
        "intitle: “index of”",
        "intitle: “index of” “.git”",
        "intitle: “index of” “.svn”",
        "inurl:”viewerframe?mode",
        "inurl:”MultiCameraFrame?Mode=Motion”",
        "intitle: “index of” “.bash_history”",
        "intext: “Last modified”",
        "intext: “Index of /”",
        "intext: “Parent Directory”",
        "inurl: “admin”",
        "inurl: “login”",
        "inurl: “login” “admin”",
        "inurl: “login” “admin” “user”",
        "intext:”privacy policy”",
        '"passwords.txt" intitle:"Index of"',
        "intext:”@gmail.com”",
    ]
    return random.choice(local_dork_query)


# ?------------------------ dork function ------------------------ #
# ?------------------------ Logo function ------------------------ #
def logo():
    # clear screen (windows/linux/mac)
    os.system("cls" if os.name == "nt" else "clear")

    # display logo
    printit(
        "─  █▀▀█ ▒█▀▄▀█ ▒█▀▀█ ─",
        center=" ",
        coledt=[1, 49, random.choice([91, 92, 93, 94, 95, 96, 97])],
        space_up=True,
    )
    printit(
        "─  █▄▀█ ▒█▒█▒█ ▒█▄▄▀ ─",
        center=" ",
        coledt=[1, 49, random.choice([91, 92, 93, 94, 95, 96, 97])],
    )
    printit(
        "─  █▄▄█ ▒█░░▒█ ▒█░▒█ ─",
        center=" ",
        coledt=[1, 49, random.choice([91, 92, 93, 94, 95, 96, 97])],
        space_down=True,
    )
    printit(
        "Oriented Modular Recognition                Omed Qarshi",
        center=" ",
        coledt=[1, 49, random.choice([91, 92, 93, 94, 95, 96, 97])],
        space_down=True,
    )


def completer(text, state):
    commands = avaliable_commands
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


# ?------------------------ Logo function ------------------------ #
# ------------------------- Main functions -------------------------- #


# ?------------------------ ALL subfunctions in one function ------------------------ #
def control_center():
    # Global variables
    global silent_mode

    # Starting control center
    if not silent_mode:
        printit(
            "[#] Initializing Oriented Modular Recognition " + Fore.LIGHTGREEN_EX +  " Try The Command 'help'" + Style.RESET_ALL,
            coledt=[1, 49, random.choice([92, 96, 97])],
            line_down=True,
            line_up=True,
            space_up=True,
        )
    # ?------------------------ exp subfunction ------------------------ #
    # EXPRESSIONS
    # ':D' -> green  | everyting is fine
    # ':)' -> blue   | info (help menu, cmd list, etc)
    # ':|' -> yellow | warning (unstable)
    # ':(' -> red    | something went wrong (error)
    # ':o' -> white  | found something (scan, search, etc)

    exp = [
        "\33[1;49;92m:D\033[0m",
        "\33[1;49;96m:)\033[0m",
        "\33[1;49;93m:|\033[0m",
        "\33[1;49;91m:(\033[0m",
        "\33[1;49;97m:o\033[0m",
    ]

    # current expression
    crt_exp = exp[0]

    exp_info = """    \33[1;49;93m> Expressions are used to show the status of the previous command\033[0m

    \33[1;49;93m> Syntax:\033[0m \33[1;49;97m[<user>@OMR]⸺ \33[1;49;96m[<expression>]\33[1;49;97m $ <command>\033[0m

    ┌────────────────────────────────────────────────────┐
    | EXPRESSIONS   | DESCRIPTION                        |
    |----------------------------------------------------|
    | \33[1;49;92m:D\033[0m            | Everything is fine                 |
    | \33[1;49;96m:)\033[0m            | Information available              |
    | \33[1;49;93m:|\033[0m            | It's a warning (remember)          |
    | \33[1;49;91m:(\033[0m            | Something went wrong               |
    | \33[1;49;97m:o\033[0m            | Scan results available             |
    └────────────────────────────────────────────────────┘"""
    # ?------------------------ exp subfunction ------------------------ #
    # ?------------------------ info subfunction ------------------------ #
    # Variables
    user = "\33[1;49;96m" + str(os.getlogin()) + "\033[0m" + " " * int(34 - len(str(os.getlogin())))
    hostname = (
        "\33[1;49;96m"
        + str(platform.node())
        + "\033[0m"
        + " " * int(34 - len(str(platform.node())))
    )
    os_name = (
        "\33[1;49;96m"
        + str(platform.system())
        + "\033[0m"
        + " " * int(34 - len(str(platform.system())))
    )
    ram = (
        "\33[1;49;96m"
        + str(psutil.virtual_memory().percent)
        + "%"
        + "\033[0m"
        + " " * int(33 - len(str(psutil.virtual_memory().percent)))
    )
    cpu = (
        "\33[1;49;96m"
        + str(psutil.cpu_percent())
        + "%"
        + "\033[0m"
        + " " * int(32 - len(str(psutil.cpu_percent())))
    )
    disk = (
        "\33[1;49;96m"
        + str(psutil.disk_usage("/").percent)
        + "%"
        + "\033[0m"
        + " " * int(33 - len(str(psutil.disk_usage("/").percent)))
    )
    sys_mac = (
        "\33[1;49;96m"
        + str(":".join(re.findall("..", "%012x" % uuid.getnode())))
        + "\033[0m"
        + " " * int(34 - len(str(":".join(re.findall("..", "%012x" % uuid.getnode())))))
    )
    arch = (
        "\33[1;49;96m"
        + str(platform.machine())
        + "\033[0m"
        + " " * int(34 - len(str(platform.machine())))
    )

    v = "3.1.0"
    ver = "\33[1;49;96m" + str(v) + "\033[0m" + " " * int(34 - len(str(v)))

    sysinfo = f"""
    ┌────────────────────────────────────────────────────┐
    | SYSTEM INFO   | DESCRIPTION                        |
    |----------------------------------------------------|
    | \33[1;49;97mUser\033[0m          | {user} |
    | \33[1;49;97mHostname\033[0m      | {hostname} |
    | \33[1;49;97mOS\033[0m            | {os_name} |
    | \33[1;49;97mArchitecture\033[0m  | {arch} |
    | \33[1;49;97mSystem MAC\033[0m    | {sys_mac} |
    |----------------------------------------------------|
    | \33[1;49;97mRAM Usage\033[0m     | {ram} |
    | \33[1;49;97mCPU Usage\033[0m     | {cpu} |
    | \33[1;49;97mDisk Usage\033[0m    | {disk} |
    └────────────────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────┐
    | Oriented Modular Recognition INFO| DESCRIPTION     |
    |----------------------------------------------------|
    | \33[1;49;97mDeveloper\033[0m     | \33[1;49;96OOmed Qarshi\033[0m                        |
    └────────────────────────────────────────────────────┘
    """
    # ?------------------------ info subfunction ------------------------ #
    # ?------------------------ help subfunction ------------------------ #
    help = """
    ┌────────────────────────────────────────────────────┐
    | COMMANDS      | DESCRIPTION                        |
    |----------------------------------------------------|
    |                 <(Basic Commands)>                 |
    |----------------------------------------------------|
    | \33[1;49;97mhelp\033[0m          | Display this help menu             | 
    | \33[1;49;97mexit/quit\033[0m     | Exit the framework                 |
    | \33[1;49;97mdork\033[0m          | Show a random google dork query \33[1;49;91m*\033[0m  |  
    | \33[1;49;97mexp\033[0m           | Show info about all available      |       
    |               | expressions                        |
    | \33[1;49;97mimage\033[0m         | Show available image reverse       |       
    |               | websites \33[1;49;91m*\033[0m                         |
    | \33[1;49;97mcheck\033[0m         | Check internet connection          |
    | \33[1;49;97mclear\033[0m         | Clear screen                       |
    | \33[1;49;97msave\033[0m          | Save output of previous scanner    |
    |               | command in a file                  |
    | \33[1;49;97mshell <cmd>\033[0m   | Execute native shell/cmd commands  |
    | \33[1;49;97minfo\033[0m          | Show info about framework & system |
    | \33[1;49;97mchange\033[0m        | Change user command input color    |
    |----------------------------------------------------|
    |                <(Scanner Commands)>                |
    |----------------------------------------------------|
    | \33[1;49;97mnumber\033[0m        | Reverse phone number lookup \33[1;49;91m*\033[0m      |
    | \33[1;49;97memail\033[0m         | Reverse email address lookup \33[1;49;91m*\033[0m     |
    | \33[1;49;97mname\033[0m          | Reverse name lookup \33[1;49;91m*\033[0m              |
    | \33[1;49;97mcoordinate\033[0m    | Reverse coordinates lookup \33[1;49;91m*\033[0m       |
    | \33[1;49;97mip\033[0m            | Reverse ip address lookup \33[1;49;91m*\033[0m        |
    | \33[1;49;97mmac\033[0m           | Reverse mac address lookup         |
    | \33[1;49;97mwhois\033[0m         | Reverse whois lookup \33[1;49;91m*\033[0m             |
    | \33[1;49;97mdns\033[0m           | Reverse or normal DNS lookup \33[1;49;91m*\033[0m     |
    | \33[1;49;97musername\033[0m      | Username lookup over multiple sites|
    |               | and social media platforms \33[1;49;91m*\033[0m       |
    └────────────────────────────────────────────────────┘
    """
    # ?------------------------ help subfunction ------------------------ #

    image = """
    ┌──────────────────────────────────────────────────────────────────────────────┐
    | SEARCH                      | DESCRIPTION OF WHAT EACH WEBSITE DOES          |
    |------------------------------------------------------------------------------|
    | https://pimeyes.com/en              | Find images on the internet            |
    |------------------------------------------------------------------------------|
    | https://labs.tib.eu/geoestimation   | Estimate geographical location of image|
    |------------------------------------------------------------------------------|
    | https://metadata2go.com             | Extract metadata from images and stuff |
    └──────────────────────────────────────────────────────────────────────────────┘
    """

    # ?------------------------ tips display ------------------------ #
    tips = [
        "Type `\33[7;49;93mhelp <command>\033[0m\33[1;49;93m` to see more info about a command",
        "Commands are `\33[7;49;93mCAP Sensitive\033[0m\33[1;49;93m`",
        "Use `\33[7;49;93mTab\033[0m\33[1;49;93m` key to auto-complete commands",
        "Try visiting the `\33[7;49;93mwebsites\033[0m\33[1;49;93m` when reverse searching",
        "You can also use `\33[7;49;93mCtrl+C\033[0m\33[1;49;93m` to exit",
        "Descriptions ending with `\33[7;49;93m*\033[0m\33[1;49;93m` need internet connection",
    ]
    # ?------------------------ tips display ------------------------ #
    # ?------------------------ save previous cmd ------------------------ #
    # Previous command
    prv_cmd = ""
    global prv_op
    global full_cmd
    # ?------------------------ save previous cmd ------------------------ #
    # ?------------------------ Autocomplete cmd ------------------------ #
    # Setting up auto-complete
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    # ?------------------------ Autocomplete cmd ------------------------ #
    # ?------------------------ cmd prompt color cmd ------------------------ #
    # Command prompt color
    cmd_color = ["\33[1;49;90m", "\33[1;49;97m"]
    crt_color = cmd_color[1]
    # ?------------------------ cmd prompt color cmd ------------------------ #
    # ?------------------------ While loop for control center ------------------------ #
    # Control center loop
    while True:
        cmd = (
            printit(
                f"\n\033[0m[{user.strip()}@OMR]⸺ [{crt_exp}] $ {crt_color}",
                input_mode=True,
                space_up=True,
            )
        ).strip()
    # ?------------------------ While loop for control center ------------------------ #
        # ?------------------------ help <cmd> ------------------------ #
        if cmd == "help":
            crt_exp = exp[1]
            prv_op = ""
            print(help)
            tip = random.choice(tips)
            print(f"\33[1;49;93m    > {tip}\033[0m")
        elif cmd == "image":
            crt_exp = exp[1]
            prv_op = ""
            print(image)
        elif cmd[:4] == "help":
            if (cmd + "#")[4] == " ":
                cmd = cmd[5:]
                if cmd == "help":
                    crt_exp = exp[1]
                    help_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mhelp\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `help`, the help menu will be displayed
    \33[1;49;92m> SYNTAX: \33[1;49;97mhelp \33[1;49;92mOR \33[1;49;97mhelp <command>
    \33[1;49;92m> EXAMPLE: \33[1;49;97mhelp \33[1;49;92mOR \33[1;49;97mhelp number
    \033[0m"""
                    print(help_help)
                elif cmd == "exit" or cmd == "quit":
                    crt_exp = exp[1]
                    exit_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mexit/\33[1;49;93mquit\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `exit` or `quit`, the program will be terminated
    \33[1;49;92m> SYNTAX: \33[1;49;97mexit \33[1;49;92mOR \33[1;49;97mquit
    \033[0m"""
                    print(exit_help)
                elif cmd == "dork":
                    crt_exp = exp[1]
                    dork_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mdork\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `dork`, a random google dork query will be displayed
    \33[1;49;92m> SYNTAX: \33[1;49;97mdork
    \033[0m"""
                    print(dork_help)
                elif cmd == "exp":
                    crt_exp = exp[1]
                    exp_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mexp\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `exp`, info about all available expressions will be displayed
    \33[1;49;92m> SYNTAX: \33[1;49;97mexp
    \033[0m"""
                    print(exp_help)
                elif cmd == "check":
                    crt_exp = exp[1]
                    check_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mcheck\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `check`, it will check for internet connection availability
    \33[1;49;92m> SYNTAX: \33[1;49;97mcheck
    \033[0m"""
                    print(check_help)
                elif cmd == "clear":
                    crt_exp = exp[1]
                    clear_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mclear\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `clear`, it will clear the screen
    \33[1;49;92m> SYNTAX: \33[1;49;97mclear
    \033[0m"""
                    print(clear_help)
                elif cmd == "save":
                    crt_exp = exp[1]
                    save_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93msave\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `save`, it will save the output of previous command
    \33[1;49;92m> SYNTAX: \33[1;49;97msave
    \33[1;49;92m> EXAMPLE: \33[1;49;97msave
    \033[0m"""
                    print(save_help)
                elif cmd[:5] == "shell":
                    crt_exp = exp[1]
                    shell_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mshell\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `shell`, it will execute given command in native shell/cmd
    \33[1;49;92m> SYNTAX: \33[1;49;97mshell <cmd>
    \33[1;49;92m> EXAMPLE: \33[1;49;97mshell ls
    \033[0m"""
                    print(shell_help)
                elif cmd == "info":
                    crt_exp = exp[1]
                    info_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93minfo\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `info`, it will show info about framework & system
    \33[1;49;92m> SYNTAX: \33[1;49;97minfo
    \033[0m"""
                    print(info_help)
                elif cmd == "change":
                    crt_exp = exp[1]
                    change_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mchange\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `change`, it will change user command input color
    \33[1;49;92m> OPTIONS: \33[1;49;97m0 -> \33[1;49;90mBlack
               \33[1;49;97m1 -> White        
    \33[1;49;92m> Default: \33[1;49;97m1
    \33[1;49;92m> SYNTAX: \33[1;49;97mchange <color_code>
    \33[1;49;92m> EXAMPLE: \33[1;49;97mchange 0
    \033[0m"""
                    print(change_help)
                elif cmd == "number":
                    crt_exp = exp[1]
                    number_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mnumber\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `number`, it will reverse lookup phone number over internet and show public info associated with it
    \33[1;49;92m> SYNTAX: \33[1;49;97mnumber <phone_number>
    \33[1;49;92m> EXAMPLE: \33[1;49;97mnumber +1234567890
    \033[0m"""
                    print(number_help)
                elif cmd == "whois":
                    crt_exp = exp[1]
                    whois_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mwhois\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `whois`, it will perform reverse whois lookup
    \33[1;49;92m> SYNTAX: \33[1;49;97mwhois <domain_name>
    \33[1;49;92m> EXAMPLE: \33[1;49;97mwhois example.com
    \033[0m"""
                    print(whois_help)
                elif cmd == "dns":
                    crt_exp = exp[1]
                    dns_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mdns\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `dns`, it will perform dns lookup for given domain name or reverse dns lookup for given ip address
    \33[1;49;92m> SYNTAX: \33[1;49;97mdns <ip_address> \33[1;49;92mOR \33[1;49;97m<domain_name>
    \33[1;49;92m> EXAMPLE: \33[1;49;97mdns 192.168.1.1 \33[1;49;92mOR \33[1;49;97mdns example.com
    \033[0m"""
                    print(dns_help)
                elif cmd == "ip":
                    crt_exp = exp[1]
                    ip_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mip\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `ip`, it will perform an ip address lookup over internet and show info about given ip address
    \33[1;49;92m> SYNTAX: \33[1;49;97mip <ip_address>
    \33[1;49;92m> EXAMPLE: \33[1;49;97mip 8.8.8.8
    \033[0m"""
                    print(ip_help)
                elif cmd == "mac":
                    crt_exp = exp[1]
                    mac_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93mmac\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `mac`, it will lookup probable vendor/manufacture of given mac address
    \33[1;49;92m> SYNTAX: \33[1;49;97mmac <mac_address>
    \33[1;49;92m> EXAMPLE: \33[1;49;97mmac ff:ff:ff:ff:ff:ff
    \033[0m"""
                    print(mac_help)
                elif cmd == "email":
                    crt_exp = exp[1]
                    email_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93memail\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `email`, it will lookup information about that email address
    \33[1;49;92m> SYNTAX: \33[1;49;97memail <email_address>
    \33[1;49;92m> EXAMPLE: \33[1;49;97maddress *****@gmail.com
    \033[0m"""
                    print(email_help)
                elif cmd == "name":
                    crt_exp = exp[1]
                    name_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93memail\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `name`, it will lookup information about that name
    \33[1;49;92m> SYNTAX: \33[1;49;97mname <first name> <last name> <city> <state>
    \33[1;49;92m> EXAMPLE: \33[1;49;97mname **** **** tracy California
    \33[1;49;93m> NOTICE: \33[1;49;97mFormat city names with spaces, like "San Francisco," as "San-Francisco" with a hyphen.
    \033[0m"""
                    print(name_help)
                elif cmd == "coordinate":
                    crt_exp = exp[1]
                    coordinate_help = """  \33[1;49;93m[+] Command Info: \33[1;49;93memail\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `coordinate`, it will lookup information about those coordinates.
    \33[1;49;92m> SYNTAX: \33[1;49;97mcoordinate <latitude> <longitude>
    \33[1;49;92m> EXAMPLE: \33[1;49;97mcoordinate 67.04957 -140.82396
    \033[0m"""
                    print(coordinate_help)
                elif cmd == 'username':
                    crt_exp = exp[1]
                    username_help = f'''  \33[1;49;93m[+] Command Info: \33[1;49;93musername\n
    \33[1;49;92m> DESCRIPTION: \33[1;49;97mWhen you type `username`, it will perform reverse username lookup over various social media platforms and check if username is associated with any account
    \33[1;49;92m> SYNTAX: \33[1;49;97musername <username>
    \33[1;49;92m> EXAMPLE: \33[1;49;97musername {user.strip()}
    \033[0m'''
                    print(username_help)
                    # ?------------------------ help <cmd> ------------------------ #
                    # ?------------------------ error messages ------------------------ #
                else:
                    crt_exp = exp[3]
                    printit(
                        "    [!] Invalid sub-command! Type `help` to see all available commands.",
                        coledt=[1, 49, 91],
                    )
            else:
                crt_exp = exp[3]
                printit(
                    "    [!] Invalid command! Type `help` to see all available commands.",
                    coledt=[1, 49, 91],
                )
            prv_op = ""
        # Basic commands
        elif cmd == "exit" or cmd == "quit":
            if not silent_mode:
                printit("    [OMR] Exiting...", coledt=[1, 49, random.choice([92, 96, 97])])
            raise KeyboardInterrupt
        elif cmd == "dork":
            crt_exp = exp[1]
            prv_op = ""
            printit("    [+] Generating random dork query...", coledt=[1, 49, 93], space_down=True)
            printit("    > " + dork_query(), coledt=[1, 49, 92])
        elif cmd == "exp":
            crt_exp = exp[1]
            prv_op = ""
            print(exp_info)
        elif cmd == "check":
            printit("    [+] Checking internet connection...", coledt=[1, 49, 93], space_down=True)
            try:
                requests.get("https://www.google.com/")
                printit("    > Internet connection is available!", coledt=[1, 49, 92])
                try:
                    public_ip = requests.get("https://httpbin.org/ip").json()[
                        "origin"
                    ]  # see if this works
                except:
                    try:
                        public_ip = requests.get("https://ident.me").text  # then this
                    except:
                        try:
                            public_ip = requests.get("https://api.ipify.org").text  # lastly this
                        except:
                            public_ip = False
                if public_ip:
                    printit(f"    > Public IP address: {public_ip}", coledt=[1, 49, 92])
                crt_exp = exp[0]
            except:
                printit("    > Internet connection is not available!", coledt=[1, 49, 91])
                printit("    > Local IP address: 127.0.0.1", coledt=[1, 49, 92])
                crt_exp = exp[3]
            prv_op = ""
        elif cmd == "clear":
            if silent_mode == False:
                crt_exp = exp[0]
                prv_op = ""
                time.sleep(0.2)
                printit("    [+] Clearing data...", coledt=[1, 49, 93], space_down=True)
                time.sleep(0.2)
                printit("    [+] Clearing screen...", coledt=[1, 49, 93], space_down=True)
                time.sleep(0.2)
                os.system("cls" if os.name == "nt" else "clear")
                logo()
            else:
                os.system("cls" if os.name == "nt" else "clear")
        elif cmd == "save":
            printit(
                "    [+] Saving output of previous command...", coledt=[1, 49, 93], space_down=True
            )
            if prv_op == "":
                printit(
                    "    > No output found! Saves output of previous scanner command only!",
                    coledt=[1, 49, 91],
                )
                crt_exp = exp[2]
            else:
                if save_output(prv_cmd):
                    crt_exp = exp[0]
                else:
                    crt_exp = exp[3]
            prv_op = ""
        elif cmd == "shell":
            crt_exp = exp[2]
            prv_op = ""
            printit(
                "    > No command found! Type `help shell` to see more info.", coledt=[1, 49, 91]
            )
        elif cmd[:5] == "shell":
            if (cmd + "#")[5] == " ":
                cmd = cmd[6:]
                exec_cmd = f"""    \33[7;49;93m[+] Executing command: {str(cmd)}\033[0m\n"""
                print(exec_cmd)

                output = os.system(cmd)
                if output == 0:
                    printit(
                        "> Command executed successfully!",
                        coledt=[7, 49, 92],
                        normaltxt_start="\n    ",
                    )
                    crt_exp = exp[0]
                else:
                    printit(
                        "> Command execution failed!", coledt=[7, 49, 91], normaltxt_start="\n    "
                    )
                    crt_exp = exp[3]
            else:
                crt_exp = exp[3]
                printit(
                    "    [!] Invalid command! Type `help` to see all available commands.",
                    coledt=[1, 49, 91],
                )
            prv_op = ""
        elif cmd == "info":
            crt_exp = exp[1]
            prv_op = ""
            print(sysinfo)
        elif cmd == "change":
            crt_exp = exp[2]
            prv_op = ""
            printit(
                "    > No color code found! Type `help change` to see more info.",
                coledt=[1, 49, 91],
            )
        elif cmd[:6] == "change":
            if (cmd + "#")[6] == " ":
                cmd = cmd[7:]
                if cmd == "0":
                    crt_color = cmd_color[0]
                    crt_exp = exp[0]
                    printit("    > Color changed successfully to BLACK!", coledt=[1, 49, 92])
                elif cmd == "1":
                    crt_color = cmd_color[1]
                    crt_exp = exp[0]
                    printit("    > Color changed successfully to WHITE!", coledt=[1, 49, 92])
                else:
                    crt_exp = exp[3]
                    printit(
                        "    [!] Invalid color code! Type `help change` to see more info.",
                        coledt=[1, 49, 91],
                    )
            else:
                crt_exp = exp[3]
                printit(
                    "    [!] Invalid command! Type `help` to see all available commands.",
                    coledt=[1, 49, 91],
                )
            prv_op = ""
        # Scanner commands
        elif cmd == "number":
            crt_exp = exp[2]
            printit(
                "    > No phone number found! Type `help number` to see more info",
                coledt=[1, 49, 91],
            )
        elif cmd[:6] == "number":
            full_cmd = cmd
            if (cmd + "#")[6] == " ":
                cmd = cmd[7:]
                printit(
                    "    [+] Performing reverse phone number lookup...",
                    coledt=[1, 49, 93],
                    space_down=True,
                )
                if number_lookup(cmd):
                    crt_exp = exp[4]
                else:
                    crt_exp = exp[3]
                    prv_op = ""
            else:
                crt_exp = exp[3]
                printit(
                    "    [!] Invalid command! Type `help` to see all available commands.",
                    coledt=[1, 49, 91],
                )
        elif cmd == "ip":
            crt_exp = exp[2]
            printit(
                "    > No ip address found! Type `help ip` to see more info", coledt=[1, 49, 91]
            )
        elif cmd[:2] == "ip":
            full_cmd = cmd
            if (cmd + "#")[2] == " ":
                cmd = cmd[3:]
                printit(
                    "    [+] Performing reverse ip address lookup...",
                    coledt=[1, 49, 93],
                    space_down=True,
                )
                if ip_lookup(cmd):
                    crt_exp = exp[4]
                else:
                    crt_exp = exp[3]
                    prv_op = ""
            else:
                crt_exp = exp[3]
                printit(
                    "    [!] Invalid command! Type `help` to see all available commands.",
                    coledt=[1, 49, 91],
                )
        elif cmd == "mac":
            crt_exp = exp[2]
            printit(
                "    > No mac address found! Type `help mac` to see more info", coledt=[1, 49, 91]
            )
        elif cmd[:3] == "mac":
            full_cmd = cmd
            if (cmd + "#")[3] == " ":
                cmd = cmd[4:]
                printit(
                    "    [+] Performing reverse mac address lookup...",
                    coledt=[1, 49, 93],
                    space_down=True,
                )
                if mac_lookup(cmd):
                    crt_exp = exp[4]
                else:
                    crt_exp = exp[3]
                    prv_op = ""
            else:
                crt_exp = exp[3]
                printit(
                    "    [!] Invalid command! Type `help` to see all available commands.",
                    coledt=[1, 49, 91],
                )
        elif cmd == "whois":
            crt_exp = exp[2]
            printit("    > No domain found! Type `help whois` to see more info", coledt=[1, 49, 91])
        elif cmd[:5] == "whois":
            full_cmd = cmd
            if (cmd + "#")[5] == " ":
                cmd = cmd[6:]
                printit(
                    "    [+] Performing reverse domain lookup...",
                    coledt=[1, 49, 93],
                    space_down=True,
                )
                if whois_lookup(cmd):
                    crt_exp = exp[4]
                else:
                    crt_exp = exp[3]
                    prv_op = ""
            else:
                crt_exp = exp[3]
                printit(
                    "    [!] Invalid command! Type `help` to see all available commands.",
                    coledt=[1, 49, 91],
                )
        elif cmd == "dns":
            crt_exp = exp[2]
            printit("    > No domain found! Type `help dns` to see more info", coledt=[1, 49, 91])
        elif cmd[:3] == "dns":
            full_cmd = cmd
            if (cmd + "#")[3] == " ":
                cmd = cmd[4:]
                printit("    [+] Performing dns lookup...", coledt=[1, 49, 93], space_down=True)
                if dns_lookup(cmd):
                    crt_exp = exp[4]
                else:
                    crt_exp = exp[3]
                    prv_op = ""
                    #! border
        elif cmd == "email":
            crt_exp = exp[2]
            printit(
                "    > No address found! Type `help email` to see more info", coledt=[1, 49, 91]
            )
        elif cmd[:5] == "email":
            full_cmd = cmd
            if (cmd + "#")[5] == " ":
                cmd = cmd[6:]
                printit(
                    "    [+] Performing reverse email lookup...",
                    coledt=[1, 49, 93],
                    space_down=True,
                )
                if email_lookup(cmd):
                    crt_exp = exp[4]
                else:
                    crt_exp = exp[3]
                    prv_op = ""
                    #! border
        elif cmd == "name":
            crt_exp = exp[2]
            printit("    > No name found! Type `help name` to see more info", coledt=[1, 49, 91])
        elif cmd.startswith("name "):
            name_data = cmd.split(" ")[1:]
            if len(name_data) == 4:
                (
                    first_name,
                    last_name,
                    city,
                    state,
                ) = name_data  # um somethings arnt accessed and im too lazy to care
                # Check if the state is a valid US state
                valid_states = [
                    "Alabama",
                    "Alaska",
                    "Arizona",
                    "Arkansas",
                    "California",
                    "Colorado",
                    "Connecticut",
                    "Delaware",
                    "Florida",
                    "Georgia",
                    "Hawaii",
                    "Idaho",
                    "Illinois",
                    "Indiana",
                    "Iowa",
                    "Kansas",
                    "Kentucky",
                    "Louisiana",
                    "Maine",
                    "Maryland",
                    "Massachusetts",
                    "Michigan",
                    "Minnesota",
                    "Mississippi",
                    "Missouri",
                    "Montana",
                    "Nebraska",
                    "Nevada",
                    "New Hampshire",
                    "New Jersey",
                    "New Mexico",
                    "New York",
                    "North Carolina",
                    "North Dakota",
                    "Ohio",
                    "Oklahoma",
                    "Oregon",
                    "Pennsylvania",
                    "Rhode Island",
                    "South Carolina",
                    "South Dakota",
                    "Tennessee",
                    "Texas",
                    "Utah",
                    "Vermont",
                    "Virginia",
                    "Washington",
                    "West Virginia",
                    "Wisconsin",
                    "Wyoming",
                    # Lowercase state names
                    "alabama",
                    "alaska",
                    "arizona",
                    "arkansas",
                    "california",
                    "colorado",
                    "connecticut",
                    "delaware",
                    "florida",
                    "georgia",
                    "hawaii",
                    "idaho",
                    "illinois",
                    "indiana",
                    "iowa",
                    "kansas",
                    "kentucky",
                    "louisiana",
                    "maine",
                    "maryland",
                    "massachusetts",
                    "michigan",
                    "minnesota",
                    "mississippi",
                    "missouri",
                    "montana",
                    "nebraska",
                    "nevada",
                    "new hampshire",
                    "new jersey",
                    "new mexico",
                    "new york",
                    "north carolina",
                    "north dakota",
                    "ohio",
                    "oklahoma",
                    "oregon",
                    "pennsylvania",
                    "rhode island",
                    "south carolina",
                    "south dakota",
                    "tennessee",
                    "texas",
                    "utah",
                    "vermont",
                    "virginia",
                    "washington",
                    "west virginia",
                    "wisconsin",
                    "wyoming",
                ]

                if state in valid_states:
                    printit(
                        "    [+] Performing reverse name lookup...",
                        coledt=[1, 49, 93],
                        space_down=True,
                    )
                    name_url1 = reverse_name_lookup(first_name, last_name, city, state)
                    time.sleep(1)
                    printit(
                        f"    [+] Reverse name lookup successful. Here is the link: {name_url1}",
                        coledt=[1, 49, 93],
                        space_down=True,
                    )
                    crt_exp = exp[4]
                    prv_op = ""
                else:
                    crt_exp = exp[3]
                    prv_op = ""
                    printit(
                        "    > Invalid State name! Make sure it is capitalized! Type `help name` to see more info",
                        coledt=[1, 49, 91],
                    )
            else:
                crt_exp = exp[2]
                printit(
                    "    > Invalid name format! Type `help name` to see more info",
                    coledt=[1, 49, 91],
                )
        elif cmd == "coordinate":
            crt_exp = exp[2]
            printit("    > Please provide both latitude and longitude. Type `help coordinate` to see more info", coledt=[1, 49, 91])
        elif cmd.startswith("coordinate "):
            coordinate_data = cmd.split(" ")[1:]
            if len(coordinate_data) == 2:
                try:
                    latitude = float(coordinate_data[0])
                    longitude = float(coordinate_data[1])
                    map_urls = generate_map_urls(latitude, longitude)
                    printit(
                        f"    [+] Searching...",
                        coledt=[1, 49, 93],
                        space_down=True,
                    )
                    time.sleep(1)
                    printit(
                        f"    [+] Loading links and searching...{map_urls}",
                        coledt=[1, 49, 93],
                        space_down=True,
                    )
                except ValueError:
                    crt_exp = exp[2]
                    printit("    > Invalid latitude or longitude format. Type `help coordinate` to see more info", coledt=[1, 49, 91])
            else:
                crt_exp = exp[2]
                printit("    > Please provide both latitude and longitude. Type `help coordinate` to see more info", coledt=[1, 49, 91])

            crt_exp = exp[3]
        elif cmd == 'username':
            crt_exp = exp[2]
            printit('    > No username found! Type `help username` to see more info', coledt=[1, 49, 91])
        elif cmd[:8] == 'username':
            full_cmd = cmd
            if (cmd+'#')[8]  == ' ':
                cmd = cmd[9:]
                printit('    [+] Performing reverse username lookup...', coledt=[1, 49, 93], space_down=True)
                if username_lookup(cmd):
                    crt_exp = exp[4]
                else:
                    crt_exp = exp[3]
                    prv_op = ''
            else:
                crt_exp = exp[3]
                printit('    [!] Invalid command! Type `help` to see all available commands.', coledt=[1, 49, 91])
        else:
            printit(
                "    [!] Invalid command! Type `help` to see all available commands.",
                coledt=[1, 49, 91],
            )
        # Updating previous command
        prv_cmd = cmd


def main():
    # Global variables
    global silent_mode

    # Checking for silent mode
    try:
        if sys.argv[1] == "-s" or sys.argv[1] == "--silent":
            silent_mode = True
    except IndexError:
        pass
    # Displaying logo
    os.system("cls" if os.name == "nt" else "clear")
    time.sleep(0.5)
    loading(loading_list)
    printit(f"[i] Installing packages...", coledt=[1, 49, 93], space_down=False)
    time.sleep(0.1)
    printit(f"[i] Installing packages..", coledt=[1, 49, 93], space_down=False)
    time.sleep(0.1)
    printit(f"[i] Installing packages.", coledt=[1, 49, 93], space_down=False)
    time.sleep(0.1)
    printit(f"[i] Finished Loading!", coledt=[1, 49, 93], space_down=False)
    time.sleep(1)
    if not silent_mode:
        logo()
    # Starting control center
    try:
        control_center()
    except KeyboardInterrupt:
        print()
        if not silent_mode:
            printit(
                "[#] Terminating Oriented Modular Recognition...",
                coledt=[1, 49, random.choice([91, 93])],
                space_down=True,
                line_down=True,
                line_up=True,
                space_up=True,
            )
            exit()
        else:
            print()
    except Exception as e:
        print()
        if not silent_mode:
            printit(f"[!] An error occured: {e}", coledt=[1, 49, 91], space_up=True)
            printit(f"[i] Please report this error", coledt=[1, 49, 93], space_down=True)
            printit(
                "[#] Terminating Oriented Modular Recognition...",
                coledt=[1, 49, random.choice([91, 93])],
                space_down=True,
                line_down=True,
                line_up=True,
                space_up=True,
            )
            exit()
        else:
            print()


if __name__ == "__main__":
    main()
