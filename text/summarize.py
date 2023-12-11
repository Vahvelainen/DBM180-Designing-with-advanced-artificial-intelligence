# !pip install transformers

from transformers import pipeline

TEXT = """
The French Revolution[a] was a period of political and societal change in France that began with the Estates General of 1789, and ended with the coup of 18 Brumaire on November 1799 and the formation of the French Consulate. Many of its ideas are considered fundamental principles of liberal democracy,[1] while its values and institutions remain central to modern French political discourse.[2]

The causes are generally agreed to be a combination of social, political and economic factors, which the Ancien Régime proved unable to manage. A financial crisis and widespread social distress led, in May 1789, to the convocation of the Estates General which was converted into a National Assembly in June. The Storming of the Bastille on 14 July led to a series of radical measures by the Assembly, among them the abolition of feudalism, state control over the Catholic Church in France, and a declaration of rights.

The next three years were dominated by the struggle for political control, exacerbated by economic depression. A series of military defeats following the outbreak of the French Revolutionary Wars in April 1792 resulted in the Insurrection of 10 August 1792. The monarchy was abolished and replaced by the French First Republic in September, while Louis XVI was executed in January 1793.

After another Paris-based revolt in June 1793, the constitution was suspended and effective political power passed from the National Convention to the Committee of Public Safety. An estimated 16,000 were executed in the subsequent Reign of Terror, which ended in July 1794. Weakened by external threats and internal opposition, the Republic was replaced in November 1795 by the Directory (1795–1799). Four years later in November 1799, the Consulate seized power in a military coup led by Napoleon Bonaparte. This is generally seen as marking the end of the Revolutionary period.

"""

summarizer = pipeline("summarization", model="philschmid/flan-t5-base-samsum")
summary = summarizer(TEXT, max_length=30)
print(summary)
