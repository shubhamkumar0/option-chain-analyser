# option-chain-analyser

This script can help option traders understand probabilistically what strike prices to choose when trading in Options.

Note: The Script uses ticker names for stocks from https://in.finance.yahoo.com/

The daily log returns for a stock{ Ln(nth day closePrice/ n-1th day close price) } follows the normal distribution.

It's std deviation can be understood as the stocks daily volatility. 

Using this along with the number of days to expiry to caluculate the +-1 Standard Deviation(SD) of the stock price, with a prability of 68%.

And the +-2 SD which can give you a 95% probability. I think I will create a short strangle at +-2 SD of HCLTECH and sip a lemonade!
