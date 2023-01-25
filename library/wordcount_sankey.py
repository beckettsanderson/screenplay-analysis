import collections
import plotly.graph_objects as go


def wordcount_sankey(show1, show2, show3, word_list=None, k=5):
    """
    Create a sankey which ties texts to the frequency of words said

    Parameters
    ----------
        show1: screenNLPlays instance
            first show to access for sankey graph
        show2: screenNLPlays instance
            second show to access for sankey graph
        show3: screenNLPlays instance
            third show to access for sankey graph
        word_list: list, default None
            words to count the frequencies of
        k: int, default 5
            the number of words from the texts to display

    Returns
    -------
        None

    """
    # create a list of the titles, and the character dictionaries
    label_list = [show1.title, show2.title, show3.title]
    show_dict = [show1.chars, show2.chars, show3.chars]

    # create a list to contain the show words per show
    show_words = []
    for x in range(len(show_dict)):

        # create list that will contain the words in a show
        mini_list = []

        # iterate through dictionary items and extract the list of words and append to mini_list
        for key, values in show_dict[x].items():
            for key2, value2 in values.items():
                for i in range(len(value2)):
                    mini_list.append(value2[i])
        show_words.append(mini_list)

    # create list to contain the frequencies of words per show
    freq_list = []
    for i in range(len(show_words)):

        # get the counts of each word per word and sort the dictionary
        frequency = collections.Counter(show_words[i])
        frequency = dict(frequency)
        a = sorted(frequency.items(), key=lambda x: x[1])

        # append to frequency_list
        freq_list.append(a)

    # if there is no word_list, we will use the k value to take the k most said words per all the shows
    if len(word_list) == 0:
        new_list = []

        # create a new list and append the show_words, and generate their frequencies
        for i in range(len(show_words)):
            for j in range(len(show_words[i])):
                new_list.append(show_words[i][j])
        frequency = collections.Counter(new_list)
        frequency = dict(frequency)

        # sort the dictionary
        a = sorted(frequency.items(), key=lambda x: x[1])
        print(a)

        # create a new list, and append the frequencies of the k most said words to the list
        word_list = []
        short = a[(-k):]
        for i in range(len(short)):
            word_list.append(short[i][0])

    print(word_list)

    # create source, target, and value lists
    source = []
    target = []
    value = []

    # For each item frequency dictionary, take the show and add that to the sources.
    # Take the word and add it to the targets.
    # Finally, take frequencies and add to the values.
    for i in range(len(word_list)):
        for j in range(len(freq_list)):
            for k in range(len(freq_list[j])):
                if freq_list[j][k][0] == word_list[i]:
                    source.append(j)

                    # must add frequencies because we have to skip over the already added shows
                    target.append(len(freq_list) + i)
                    value.append(freq_list[j][k][1])

    # create sankey
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label_list + word_list,
            color=["blue", "red", "green"]
        ),

        link=dict(
            source=source,
            target=target,
            value=value,

        ))])

    fig.update_layout(title_text="Frequency of Shows and Common Words", font_size=20)
    fig.write_image("Wordcount_Sankey.png")
    fig.show()
