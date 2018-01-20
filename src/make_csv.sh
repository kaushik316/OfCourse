#!/bin/bash

echo "NAME,ALIAS,PATH,DESCRIPTION" > courses.csv ;

for CSV in Departments/*.csv
do
  tail -n +2 $CSV >> courses.csv
done
