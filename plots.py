from matplotlib import pyplot as plt

y_yt_orig = [0.75, 0.70, 0.60, 0.55,0.50,0.45,0.40,0.35,0.30,0.30,0.25,0.20]
y_yt_hyp = [0.85,0.75,0.65,0.55,0.45,0.45,0.35,0.30,0.30,0.30,0.25,0.25]
y_yt_BA = [0.90,0.85,0.80,0.70,0.60,0.55,0.45,0.40,0.40,0.40,0.40,0.40]

x = [0,1,2,3,4,5,6,7,8,9,10,11]


plt.plot(x, y_yt_orig, 'r')
plt.plot(x, y_yt_hyp, 'b')
plt.plot(x, y_yt_BA, 'g')
plt.title("youtube")
plt.ylabel("elite size (n^y)")
plt.xlabel("elite influence factor (2^x)")
plt.show()