cd task_high_energy/

for dir in `ls .`
do
	if [ -d $dir ];
	then
		cd $dir/

		for((i=1;i<=20;i++))
		do
		    cat 2019-09-?????????$i.log | grep Walk | cut -f4 -d' ' > "$i.log"; 
		done
		python3 /home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/priority/same/collision.py

		cd ../
	fi
done
