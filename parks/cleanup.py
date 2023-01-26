import re
import json
# words to be*- ignored in indexing
INDEX_IGNORE = (
    "a",
    "an",
    "and",
    "&",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "he",
    "in",
    "is",
    "it",
    "its",
    "of",
    "on",
    "that",
    "the",
    "to",
    "was",
    "were",
    "will",
    "with",
    "chicago",
    "park",
    "parks",
)


def normalize_address(address):
    """
    This function takes an address and returns a normalized
    version of the address with extra whitespace removed.
    Parameters:
        * address:  a string representing an address
    Returns:
        A string representing the address with extra whitespace removed.
    """
    answer = re.sub('\s+', ' ', address.strip())
    return answer


def tokenize(park):
    """
    This function takes a dictionary representing a park and returns a
    list of tokens that can be used to search for the park.
    The tokens should be a combination of the park's name, history, and
    description.
    All tokens should be normalized to lowercase, with punctuation removed as
    described in README.md.
    Tokens that match INDEX_IGNORE should be ignored.
    Parameters:
        * park:  a dictionary representing a park
    Returns:
        A list of tokens that can be used to search for the park.
    """
    answer = []
    for k, v in park.items():
        if k == 'address':
            park[k] = normalize_address(v)
        elif k == 'name' or k == 'history' or k == 'description':
            v = re.sub('[!.,\'\"?:]', '', v)
            v = v.lower()
            temp = v.split()
            for tok in temp:
                if tok not in INDEX_IGNORE:
                    answer.append(tok)
    answer = list(set(answer))
    park['tokens'] = answer

    return park['tokens']

def clean():
    """
    This function loads the parks.json file and writes a new file
    named normalized_parks.json that contains a normalized version
    of the parks data.
    """
    data = []
    with open("parks.json", "r") as f:
        data = json.load(f)

    for dic in data:
        tokenize(dic)

    with open("normalized_parks.json", "w") as f:
        json.dump(data, f, indent = 1)

'''
a =  {
  "url": "https://scrapple.fly.dev/parks/1",
  "name": "Abbott (Robert) Park",
  "address": "49 E. 95th St. Chicago, IL 60628",
  "description": "Located in the Roseland Community Area, Abbott Park totals 25 acres and features a multi-purpose room and game room. Outside, the park offers four baseball diamonds, basketball, track and tennis courts, swimming pool, and two sprinklers. Many of these spaces are available for rental including our multi-purpose room and game room.Park-goers can participate in seasonal sports, cheerleading, aerobics, senior and teen clubs. On the cultural side, Abbott Park offers dance, music and movement. After school programs are offered throughout the school year, and during the summer youth can attend the Park District\u2019s popular six-week day camp.Specialty camps, including Sports Camp, are also offered in the summer.In addition to programs, Abbott Park hosts fun special events throughout the year for the entire family including holiday events.",
  "history": "The Chicago Park District acquired the site of Abbott Park as part of a ten-year plan to increase recreational opportunities in under-served neighborhoods in post-World War II Chicago. In 1947, the Citizens Advisory Committee on Park Sites recommended the creation of a park to serve the rapidly growing African-American community near 95th Street and Michigan Avenue. The Park District purchased the property southeast of that intersection in 1949 and 1950, and built a swimming pool and recreational facility the following year. In 1956, the District sold a portion of the parkland to the Board of Education for use as Harlan High School.Robert Sengstacke Abbott (1868-1940), for whom the park is named, founded the influential Chicago Defender in 1905. Born in Georgia, Abbott received his education in southern schools, and graduated from Chicago's Kent College of Law. He was the only African-American in the class of 1899. Abbott's lofty goal was to eliminate racial prejudice through his newspaper. To promote racial equality, Abbott and his Chicago Defender newspaper urged southern blacks to migrate to Chicago and other northern cities for greater economic opportunity. By 1918, the influential newspaper had a national circulation of 125,000, making it the largest-selling black newspaper in the country. President of his Abbott Publishing Company, Abbott was also active in civic affairs. He served on Governor Frank O. Lowden's Race Relations Committee in 1919, on the Board of Commissioners of the Chicago World's Fair in 1934, and on the boards of the Art Institute, the Field Museum, and the Chicago Historical Society."
 }
tokenize(a)
print(a)
'''
clean()