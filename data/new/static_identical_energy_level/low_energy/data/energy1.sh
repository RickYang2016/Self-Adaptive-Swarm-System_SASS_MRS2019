for((i=1;i<=10;i++))
do
    cat 2019-03-?????????$i.log | grep Energy | cut -f2 -d']' > a
    tail -n +9  a > energy$i.txt
    rm a
done

for((i=1;i<=10;i++))
do
    cat 2019-03-?????????$i.log | grep Walk | cut -f4 -d' ' > walk$i.txt
done

for((i=1;i<=10;i++))
do
    cat 2019-03-?????????$i.log | grep Walk | cut -f2 -d' ' | cut -f1 -d':' > time$i.txt
done

paste time3.txt energy*.txt > time_energy.txt

paste time3.txt walk*.txt > time_walk.txt