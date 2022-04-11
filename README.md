# Independent Component Analysis: Cocktail Party Data

The cocktail party problem is a classic problem of audio signal separation. The traditional problem is that in a party with multiple individuals speaking, multiple people may be speaking. While it may be possible for an observer to isolate a given conversation, it is difficult for a computer to separate one speaker or conversation from another. One statistical method used to tackle this problem of signal separation is independent component analysis (ICA). The rest of this paper is designed as follows: a theoretical background to ICA, its applications to a simulated dataset, and its applications to a sample of Amazon's Dinner Party Corpus.

# Application: Amazon Dinner Party Corpus

I applied ICA to a public dataset from Amazon called the Dinner Party Corpus (DiPCo), which is licensed for use and sharing under the CDLA-Permissive license (https://cdla.dev/permissive-1-0/).. In this dataset, four participants are recorded having a dinner party in a room with five microphone arrays placed in various locations around the room. 

![](data/room_layout.jfif)

