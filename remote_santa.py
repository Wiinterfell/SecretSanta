#!/usr/bin/env python

import csv
import json
import random

def bad_match(match_dict,exc_dict):
    for santa,target in match_dict.items():
        if target in exc_dict[santa]:
            print target, santa
            return True
    return False

def random_match(email_list):
    people_list = list(email_list)
    random.shuffle(people_list)
    match_dict = dict()
    for i in range(len(people_list)-1):
        match_dict[people_list[i]] = people_list[i+1]
    match_dict[people_list[-1]] = people_list[0]
    return match_dict

def get_match(exc_dict):
    email_list = exc_dict.keys()
    match_dict = random_match(email_list)
    while bad_match(match_dict,exc_dict):
        match_dict = random_match(email_list)
    return match_dict

def load_csv(csv_filename):
    email_to_name = dict()
    email_to_line1 = dict()
    email_to_line2 = dict()
    email_to_postal = dict()
    email_to_city = dict()
    email_to_number = dict()
    email_to_comment = dict()
    exclusions = dict()
    with open(csv_filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            email = row['email'].strip()
            name = row['firstname'].strip() + ' ' + row['lastname'].strip()
            exe = [row['exclude'].strip()]

            line1 = row['address_line_one_secret_santa_2020'].strip()
            line2 = row['address_line_two_secret_santa_2020'].strip()
            postal = row['address_line_postalcode_secret_santa_2020'].strip()
            city = row['address_line_city_secret_santa_2020'].strip()
            number = row['address_line_number_secret_santa_2020'].strip()
            comment = row['secret_santa_address_2020'].strip()

            email_to_name[email] = name

            email_to_line1[email] = line1
            email_to_line2[email] = line2
            email_to_postal[email] = postal
            email_to_city[email] = city
            email_to_number[email] = number
            email_to_comment[email] = comment

            exclusions[email] = exe
            #print(name + ' ' + email + ' ' + exe[0])
    return (email_to_name, exclusions, email_to_line1, email_to_line2, email_to_postal, email_to_city, email_to_number, email_to_comment)

if __name__ == '__main__':
    email_to_name, exc_dict, email_to_line1, email_to_line2, email_to_postal, email_to_city, email_to_number, email_to_comment = load_csv('2020.csv')
    match_list = get_match(exc_dict)
    # save match list
    #json.dump(match_list,open('match_list.json','w'),indent=2)
    # save email to name dict
    #json.dump(email_to_name,open('email_to_name.json','w'),indent=2)

    with open('output2020.csv', 'wb') as fout:
        csvout = csv.writer(fout)
        csvout.writerow( ['email'] + ['Santa_name'] + ['Santa_assignee_email_2020'] +  ['Santa_assignee_2020_line_one'] + ['Santa_assignee_2020_line_two'] + ['Santa_assignee_2020_line_postalcode'] + ['Santa_assignee_2020_line_city'] + ['Santa_assignee_2020_line_number'] + ['Santa_assignee_2020_line_comment'])
        for person in match_list:
            #print person
            #print match_list[person]
            csvout.writerow( [person] + [match_list[person]] + [email_to_name[match_list[person]]] + [email_to_line1[match_list[person]]] + [email_to_line2[match_list[person]]] + [email_to_postal[match_list[person]]] + [email_to_city[match_list[person]]] + [email_to_number[match_list[person]]] + [email_to_comment[match_list[person]]])


