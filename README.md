# Screenplay Analysis

Our NLP project involves working with TV script data regarding the frequency of words and sentiment analysis to construct sankey diagrams, word clouds, and line plots. The 
data source we selected to work with was screenplays.io. This website provides hundreds of screenplays from various movies and television shows. Screenplays can be 
downloaded in a PDF format (though we scraped them directly from the website), and contain setting descriptions, screen directions, and the text said by each 
character. By entering in the title of the show, the program obtains the PDF file of the show and converts it to a pypdf object.

One of the visualizations constructed was a sankey diagram, linking the shows to the most frequently said words. The width of each link between a show and a 
word in the diagram represents the frequency of how often the word was said in the show.
The second visualization used matplotlib subplots to plot three wordcloud plots. For each show, we displayed the words with the highest frequency count with the 
font size as an indicator of how often a word was said (with larger words having a higher frequency).
Our third visualization was sentiment analysis on various shows. For each episode in the show, the sentiment score was calculated using the positive and negative 
words text files, and then the values were displayed together on a line plot.
