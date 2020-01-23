cd data/

for((i=1;i<=20;i++))
do
    cat 2019-03-?????????$i.log | grep Walk | cut -f4 -d' ' > "$i.log"; 
done
python3 /home/rick/SRSS/data/new/static_identical_energy_level/low_energy/collision.py
