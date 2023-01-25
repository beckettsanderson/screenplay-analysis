import requests
import urllib.request
import PyPDF2
import io
import string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

OTHER_STOP_WORDS = ['know', 'get', 'like', 'im', 'oh', 'yes', 'don\'t', 'want', 'okay',
                    'i\'m', 'youre', 'thats', 'that\'s', 'dont', 'yeah', 'go', 'got']
STOPS = list(set(stopwords.words('english'))) + OTHER_STOP_WORDS


class screenNLPlays:

    def __init__(self, show_name, char_lst=[], more_stops=None):
        self.title = show_name
        self.screenplays = {}
        self.words = {}

        # add extra stop words for an individual show on top of nltk stopwords
        self.stops = STOPS + [x.lower() for x in char_lst]
        if more_stops:
            self.stops += [x.lower() for x in more_stops]

        self.char_lst = [x.upper() for x in char_lst]
        self.chars = {}

        # calls get_screenplays to add the show data to the class instance when initiated
        self.get_screenplays()

        # call to add the script words for each show when initiated
        self.get_all_words()

    def get_screenplays(self):
        """
        Gets all scripts of a given show from screenplays.io and returns a dictionary.

        Parameters
        ----------

        Returns
        -------
        self.screenplays : dict
            A dictionary where each key is an episode number, and each value is a pdf object of that episode's script.
        """

        # get BeautifulSoup for show
        title = '-'.join(self.title.lower().split(' '))
        url = f'https://screenplays.io/screenplay/{title}'
        soup = BeautifulSoup(requests.get(url).text, features='html.parser')

        # get episode numbers
        h2 = [x.text for x in soup.find_all('h2')]
        eps = [int(x.split(':')[0].split(' ')[-1]) for x in h2]

        # get pdf for main script
        main = soup.find('div', class_='css-h4w0m4')
        link = main.find('a', class_='button css-17g225z')
        href = link.attrs['href']
        splt_href = href.split('/')
        last_line = '%20'.join(splt_href[-1].split(' '))
        url = '/'.join(splt_href[:-1]) + '/' + last_line
        req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
        remote_file = urllib.request.urlopen(req).read()
        remote_file_bytes = io.BytesIO(remote_file)
        main_pdf = PyPDF2.PdfFileReader(remote_file_bytes, strict=False)

        # get links of each other episode of show
        divs = soup.find('div', class_='css-m3aich')
        all_links = divs.find_all('a', class_='button css-17g225z')
        pdf_lst = []

        # get pdf for each episode and append to list
        for link in all_links:
            href = link.attrs['href']
            splt_href = href.split('/')
            last_line = '%20'.join(splt_href[-1].split(' '))
            url = '/'.join(splt_href[:-1]) + '/' + last_line
            req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
            remote_file = urllib.request.urlopen(req).read()
            remote_file_bytes = io.BytesIO(remote_file)
            pdfdoc_remote = PyPDF2.PdfFileReader(remote_file_bytes, strict=False)
            pdf_lst.append(pdfdoc_remote)

        # remove first episode since there might be duplicate of main script
        pdf_lst.pop(0)
        pdf_lst.insert(0, main_pdf)

        # create dictionary with episode as key, script as value
        screenplay_dict = {eps[i]: pdf_lst[i] for i in range(len(pdf_lst))}
        self.screenplays = screenplay_dict

    def get_all_words(self):
        """
        Gets a dictionary of all words by episode and adds it to self.words

        Parameters
        ----------

        Returns
        -------
        None
        """
        if not self.screenplays:
            raise ValueError('No screenplays were loaded in')

        words = {}
        for episode, script in self.screenplays.items():
            words[episode] = []
            for i in range(script.numPages):

                # split each page into lines
                page_text = script.getPage(i).extractText()
                page_lst = page_text.split('\n')

                for line in page_lst:
                    line = line.split(' ')
                    line = [x.translate(str.maketrans('', '', string.punctuation)) for x in line]
                    line = [x for x in line if x]
                    words[episode] += [x.lower() for x in line]

        # remove the stopwords from the all words data
        self.words = self.remove_stop_words(words, by_ep=True)

    def remove_stop_words(self, words_dict, by_ep=False):
        """
        Takes a dictionary containing all words spoken in a show and removes commonly spoken words to allow for better
        analysis.

        Parameters
        ----------
        words_dict : dict of dicts of lists
            dictionary of all the words spoken in a show organized by character and episode
        by_ep : bool
            boolean stating the format from which the function is removing the words

        Returns
        -------
        words_dict : dict of dicts of lists
            dictionary of all the words spoken in a show organized by character and episode, but with stop words removed

        """
        words_to_remove = []

        if by_ep:
            # set of for loops to loop through each word spoken in the text
            for ep in words_dict:
                for word in words_dict[ep]:

                    # checks if word is a stopword and if so adds it to a stored list
                    if word.lower() in self.stops:
                        words_to_remove.append(word)

                # loops through words spoken and removes the stored words to delete
                for word in words_to_remove:
                    words_dict[ep].remove(word)

                # resets the list to empty for the next episodes words
                words_to_remove = []

        else:
            # set of for loops to loop through each word spoken in the text
            for char in words_dict:
                for ep in words_dict[char]:
                    for word in words_dict[char][ep]:

                        # checks if word is a stopword and if so adds it to a stored list
                        if word.lower() in self.stops:
                            words_to_remove.append(word)

                    # loops through words spoken and removes the stored words to delete
                    for word in words_to_remove:
                        words_dict[char][ep].remove(word)

                    # resets the list to empty for the next episodes words
                    words_to_remove = []

        return words_dict

    def get_char_data(self):
        """
        Given a list of characters, gets all the words they speak throughout the show by episode.

        Parameters
        ----------

        Returns
        -------
        self.chars : dict of dicts of lists
            A nested dictionary where each key is a character. Each character's value is a dictionary, whose keys are
            episode numbers and values are a list of all the words that character speaks in the corresponding episode.
        """

        # create dictionary for characters and episodes
        char_data = {char: {ep: [] for ep in self.screenplays} for char in self.char_lst}

        # iterate through every script
        for episode_num, script in self.screenplays.items():

            # iterate through each page
            for i in range(script.numPages):

                # split each page into lines
                page_text = script.getPage(i).extractText()
                page_lst = page_text.split('\n')
                line_num = 0

                # repeat until we run out of lines
                while line_num < len(page_lst):

                    # if line is all caps
                    if page_lst[line_num].upper() == page_lst[line_num]:

                        # in case no chars are in uppercase line, check at end
                        curr_line = line_num

                        # check which character is speaking
                        for char in self.char_lst:
                            if char in page_lst[line_num]:
                                line_num += 1

                                # add all the lines until someone else is speaking
                                while line_num < len(page_lst) and page_lst[line_num] != page_lst[line_num].upper():
                                    words = page_lst[line_num].split(' ')
                                    words = [x.translate(str.maketrans('', '', string.punctuation)) for x in words]
                                    words = [x for x in words if x]
                                    char_data[char][episode_num] += words
                                    line_num += 1

                                # stop checking characters
                                break

                        # if it wasn't a character speaking, skip it
                        if line_num == curr_line:
                            line_num += 1

                    # not uppercase, skip line
                    else:
                        line_num += 1

        char_data = self.remove_stop_words(char_data)
        self.chars = char_data
