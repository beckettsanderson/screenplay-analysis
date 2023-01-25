import matplotlib.pyplot as plt
import pprint as pp

NEG = "negative-words.txt"
POS = "positive-words.txt"


def read_text(filename):
    """
    Reads in a file separated by new line characters and returns the data in a list

    Parameters
    ----------
        filename : str
            the string containing the .txt file containing the data

    Returns
    -------
        file_data : list
            list of all the lines in a file

    """
    # opens the file
    with open(filename) as file:

        # reads the data into a list
        file_data = file.read().split("\n")

    return file_data


def get_sentiment(show):
    """
    Takes a show and uses sentiment analysis to get sentiment scores for the words spoken in each episode of the show.

    Parameters
    ----------
        show : screenNLPlays instance
            the show from which to access the chars dictionary

    Returns
    -------
        sent_dict : dict
            dictionary containing a list of episodes and a list of sentiment scores for a show

    """
    # create dictionary containing a list of episodes and a list of sentiment scores
    sent_dict = {"eps": [],
                 "sent_score": []}

    # read in the positive and negative words for sentiment analysis
    pos_words = read_text(POS)
    neg_words = read_text(NEG)

    ep_num = 0

    # loop through each word spoken in each episode
    for ep in show.words:

        # adjust storage vals for each episode
        ep_num += 1
        sentiment_score = 0

        for word in show.words[ep]:

            # checks if the word is in positive or negative words and adjusts sentiment score based on that
            if word.lower() in pos_words:
                sentiment_score += 1

            elif word.lower() in neg_words:
                sentiment_score -= 1

        # adds the values to the dictionary
        sent_dict['eps'].append(ep_num)
        sent_dict['sent_score'].append(sentiment_score)

    return sent_dict


def sentiment_plot(show_lst):
    """
    Creates three wordcloud subplots to compare three different shows for their most common words.

    Parameters
    ----------
        show_lst : list of screenNLPlays instances
            list of shows from which to access the words dictionary

    Returns
    -------
        None
    """
    # create figure and axes
    fig, ax = plt.subplots()

    # plot each show's sentiment scores by episode
    for show in show_lst:

        # get sentiment scores for each episode of each show
        show_sent = get_sentiment(show)
        pp.pprint(show_sent)

        # create line for each show
        ax.plot(show_sent['eps'], show_sent['sent_score'], label=show.title)

    # create the legend for the shows
    ax.legend(title='Shows:')

    # title and axis organization
    ax.set_title('Show Comparison of Sentiment Score Over Time')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Sentiment Score')

    plt.savefig("Sentiment_Over_Time.png", dpi=1200, format='png')
    plt.show()
