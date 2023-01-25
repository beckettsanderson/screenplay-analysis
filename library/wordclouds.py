import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter


def get_word_counts(show):
    """
    Creates a dictionary where every word is an index in the dictionary and references to the number of occurrences
    of that word in the text.

    Parameters
    ----------
        show : screenNLPlays instance
            the show from which to access the chars dictionary

    Returns
    -------
        count_dict : dictionary
            dictionary of all the words spoken in a show organized by each word and the number of times spoken

    """
    word_lst = []

    # loop through all words and add them to list for Counter package
    for ep in show.words:
        word_lst = word_lst + show.words[ep]

    # create dictionary with Counter package
    count_dict = Counter(word_lst)

    return count_dict


def wordcloud_subplots(show1, show2, show3):
    """
    Creates three wordcloud subplots to compare three different shows for their most common words.

    Parameters
    ----------
        show1 : screenNLPlays instance
            the first show from which to access the chars dictionary
        show2 : screenNLPlays instance
            the first show from which to access the chars dictionary
        show3 : screenNLPlays instance
            the first show from which to access the chars dictionary

    Returns
    -------
        None
    """
    # call a function to get collection of words in a format to input into wordcloud for each show
    count_dict_show1 = get_word_counts(show1)
    count_dict_show2 = get_word_counts(show2)
    count_dict_show3 = get_word_counts(show3)

    # create a wordcloud image from show1 dialogue and plot in a subplot with the corresponding show title
    wordcloud_show1 = WordCloud().generate_from_frequencies(count_dict_show1)
    plt.subplot(3, 1, 1)
    plt.imshow(wordcloud_show1)
    plt.axis("off")
    plt.title(show1.title, loc='left')

    # create a wordcloud image from show2 dialogue and plot in a subplot with the corresponding show title
    wordcloud_show2 = WordCloud().generate_from_frequencies(count_dict_show2)
    plt.subplot(3, 1, 2)
    plt.imshow(wordcloud_show2)
    plt.axis("off")
    plt.title(show2.title, loc='left')

    # create a wordcloud image from show3 dialogue and plot in a subplot with the corresponding show title
    wordcloud_show3 = WordCloud().generate_from_frequencies(count_dict_show3)
    plt.subplot(3, 1, 3)
    plt.imshow(wordcloud_show3)
    plt.axis("off")
    plt.title(show3.title, loc='left')

    plt.savefig("Wordclouds_vert.png", dpi=2400, format='png')
    plt.show(dpi=2400)
