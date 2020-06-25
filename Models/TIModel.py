from Controllers.TAlibWrapper import *


# Bollinger Bands strategy
def BBANDS_close_diff(CLOSE_SERIES, NORMALIZED=False, ROC=False):
	BBANDS_data = BBANDS(CLOSE_SERIES, SMOOTH=True)

	if not NORMALIZED:
		DIFFcloseNupBB_data = DIFF(CLOSE_SERIES, BBANDS_data[0])[0]
		DIFFcloseNloBB_data = DIFF(BBANDS_data[2], CLOSE_SERIES)[0]
	else:
		DIFFcloseNupBB_data = DIFF(CLOSE_SERIES, BBANDS_data[0])[1]
		DIFFcloseNloBB_data = DIFF(BBANDS_data[2], CLOSE_SERIES)[1]

	for i in range(len(DIFFcloseNupBB_data)):
		if DIFFcloseNupBB_data[i] < 0.0:
			DIFFcloseNupBB_data[i] = None
		if DIFFcloseNloBB_data[i] < 0.0:
			DIFFcloseNloBB_data[i] = None

	if not ROC:
		return DIFFcloseNupBB_data, DIFFcloseNloBB_data

	for i in range(len(DIFFcloseNupBB_data) - 1, -1, -1):
		if i == 0:
			continue

		if DIFFcloseNupBB_data[i] is not None and DIFFcloseNupBB_data[i - 1] is not None:
			DIFFcloseNupBB_data[i] = ((DIFFcloseNupBB_data[i] / DIFFcloseNupBB_data[i - 1]) - 1) * 100

		if DIFFcloseNloBB_data[i] is not None and DIFFcloseNloBB_data[i - 1] is not None:
			DIFFcloseNloBB_data[i] = ((DIFFcloseNloBB_data[i] / DIFFcloseNloBB_data[i - 1]) - 1) * 100

	return DIFFcloseNupBB_data, DIFFcloseNloBB_data


# MACD Signal line strategy
def MACD_NORMALIZED(CLOSE_SERIES):
	# Not working as intended
	MACD_data = MACD(CLOSE_SERIES)
	MACD_main = MACD_data[0]
	MACD_signal = MACD_data[1]

	SMA_close = SMA(CLOSE_SERIES)
	MACD_main_normalized = []
	MACD_signal_normalized = []
	for i in range(len(CLOSE_SERIES)):
		n_main = 100.0 * MACD_main[i] / CLOSE_SERIES[i]
		n_signal = 100.0 * MACD_signal[i] / CLOSE_SERIES[i]

		MACD_main_normalized.append(n_main)
		MACD_signal_normalized.append(n_signal)
	return MACD_main_normalized, MACD_signal_normalized

def MACD_signal_diff(CLOSE_SERIES, NORMALIZED=False, ROC=False):
	MACD_data = MACD(CLOSE_SERIES)
	MACD_main = MACD_data[0]
	MACD_signal = MACD_data[1]

	if not NORMALIZED:
		return DIFF(MACD_main, MACD_signal)[0]
	else:
		return DIFF(MACD_main, MACD_signal)[1]

# TODO: BBANDS strat: when close value goes below lower BBand, wait until close rate of change starts going positive and buy,
#  then wait until close value goes above upper BBand and rate of change gets negative. If at that point you get profit - sell.
#  Else, if at any point upper BBand dips below the value of lower BBand at the time of buy, sell at the next peak above
#  the upper BBand, no matter if you get profit.

# TODO: MACD strat: when MACD signal line dips below main MACD line and reaches atleast -0.01, buy. Vice versa when
#  peaking 0.01 difference above the main value.

# TODO: try mixed BBANDS and MACD strat.

