cd 10/

for dir in `ls .`
do
	if [ -d $dir ];
	then
		cd $dir/

		for((i=1;i<=10;i++))
		do
		    cat 2019-08-?????????$i.log | grep Walk | cut -f4 -d' ' > "$i.log"; 
		done
		python3 /home/rick/Documents/research/SRSS/data/ICRA_data/static_tasks/collision/collision10.py

		cd ../
	fi
done
