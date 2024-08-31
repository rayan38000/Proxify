# 🚀 Proxify - AIO tool for proxies

**Proxify** is a user-friendly tool for managing and checking proxies. Even without technical expertise, you can easily scrape, verify, and analyze HTTP, SOCKS4, and SOCKS5 proxies.

---

![Proxify Banner](https://media.discordapp.net/attachments/1159608437118865541/1279237669007659048/image.png?ex=66d3b66b&is=66d264eb&hm=5c6517d838295b680c8c756a4997219194e8f30880675d4f2dfd0b3da546b1be&=&format=webp&quality=lossless)


<p align="center"><a href='https://mega.nz/file/cDVU1ZbQ#bLIN9zsLEn0q8QbR-H0FcFpFp1B40RnUJncwuDOiGJY'>CLICK HERE FOR WATCHING VIDEO</a></p>


---

## 🛠️ Features

- **Proxy Scraper**: Scrape HTTP, SOCKS4, and SOCKS5 proxies from various sources.
- **Proxy Checker**: Verify the quality, anonymity, and geolocation of your proxies.
- **Proxy Information**: Gather detailed information about a specific proxy, including headers and anonymity level.

---

## 🧠 Reminder

| Proxy Type    | Description | Advantages | Disadvantages |
|---------------|-------------|------------|---------------|
| **Transparent** | Transparent proxies send the original IP address of the user to the target server. They are mainly used for content filtering and caching. | - Easy to set up<br>- Good for caching performance | - Does not protect privacy<br>- Easily identifiable |
| **Anonymous**   | Anonymous proxies hide the user's IP address but send the proxy identifier to the target server. This makes the user less traceable, but the proxy is still identifiable. | - Improves privacy compared to transparent proxies<br>- Reduces traceability | - Identifiable as a proxy<br>- Does not guarantee total anonymity |
| **Elite**       | Elite (or high-anonymity) proxies completely hide the user's IP address and do not reveal that traffic is passing through a proxy. They offer the highest level of privacy and anonymity. | - Highest level of privacy<br>- Not identifiable as a proxy<br>- Good protection against tracking | - May be slower due to additional anonymity layer<br>- Often more expensive |

---

## 🌐 Proxy Scraper

The Proxy Scraper is designed to fetch and collect proxies from various online sources. The URLs used for scraping these proxies are stored in text files within a folder named `links`. There are three specific text files based on the type of proxies:

- **http.txt**: Contains URLs for scraping HTTP proxies.
- **socks4.txt**: Contains URLs for scraping SOCKS4 proxies.
- **socks5.txt**: Contains URLs for scraping SOCKS5 proxies.

These files make it easy for users to manage and update the tool themselves. You can enhance the Proxy Scraper by adding new URLs (proxy list sources you find online) to the respective text files. Additionally, you can maintain the quality of your proxy lists by removing any dead or non-functional URLs from these files.

By simply editing these text files, users have full control over the sources the scraper uses, ensuring they always have access to the most up-to-date and reliable proxies.




## ✅ Proxy Checker
This section of the Proxify project is dedicated to checking and analyzing proxies. The feature checks the status and characteristics of proxies, including their type, speed, anonymity, and geographic location. Here is an overview of this feature:

![Proxy Checker](https://media.discordapp.net/attachments/1159608437118865541/1279239709125513277/image.png?ex=66d3b851&is=66d266d1&hm=0cf34d5af3bfcbf2b7cb2a0cf28bb9816739899ce34949691e8374db091913c2&=&format=webp&quality=lossless&width=1100&height=644)

**Supported Proxy Types**: HTTP, SOCKS4, SOCKS5.

**Verification Method**: The program sends requests through the proxies to a judge and analyzes the proxy header (found in the judge's response) to determine if the proxy is functional and whether it is anonymous or transparent.

I did not add features to differentiate between elite proxies and anonymous proxies because it is difficult to distinguish them. I tried to compare headers between these two types of proxies, but there is not much concrete information available in this area. It is indeed possible to check for the absence of certain headers that might indicate an elite proxy, but this verification remains insufficient. Out of caution, I preferred not to handle it.

## 🔎 Proxy Information

The Proxy Information feature allows you to gather detailed information about a specific proxy, including its headers and anonymity level. This functionality is particularly useful for analyzing and verifying proxies to ensure they meet your requirements. Here’s a breakdown of what this feature offers:

Features:
- Header Analysis: Retrieve and analyze the HTTP headers sent by the proxy to understand its behavior and how it handles requests.
- Anonymity Level: Determine the type of proxy (Transparent, Anonymous, or Elite) based on the information available in the headers.
- Geolocation: Identify the geographical location of the proxy server to verify its location-based restrictions or preferences.
- Performance Metrics: Evaluate the response time and reliability of the proxy to ensure it performs well under different conditions.

---

## 📋 Requirements

- Python 3
- The following Python libraries:
  - `requests`
  - `colorama`
  - `pystyle`
  - `beautifulsoup4`
  - `tqdm`
  - `pandas`
  - `tabulate`

I list these modules, but you will not need to install them manually. Upon launch, the tool checks that all the modules are properly installed, and if not, it will install them automatically.

