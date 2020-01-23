for((i=1;i<=20;i++))
do
    cat 2019-09-?????????$i.log | grep Energy | cut -f2 -d']' > a
    tail -n +9  a > energy$i.txt
    rm a
done

for((i=1;i<=20;i++))
do
    cat 2019-09-?????????$i.log | grep Walk | cut -f4 -d' ' > walk$i.txt
done

for((i=1;i<=20;i++))
do
    cat 2019-09-?????????$i.log | grep Energy | cut -f1 -d'[' > b
    tail -n +9  b > c
    cat c | cut -f2-3 -d':' > time$i.txt
    rm b c
done

for((i=1;i<=20;i++))
do
    cat 2019-09-?????????$i.log | grep Walk | cut -f2 -d' ' | cut -f1 -d':' > step$i.txt
done

paste step3.txt time3.txt energy*.txt > time_energy.txt

paste step3.txt time3.txt walk*.txt > time_walk.txt
