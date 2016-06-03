# final_dk_project

Draftkings Automator Project

General Idea: use trained regression model to generate fantasy point projection rankings; select best lineup from these rankings with cost constraints in mind.

lineup_picker - currently does the brunt work of selecting the best lineup given rankings and costs.

scraper - used to generate rankings for today's players using weights generated from classifier

classifier - used to update weights for regression model; uses data collected from data_miner

data_miner - scrapes web for training data
