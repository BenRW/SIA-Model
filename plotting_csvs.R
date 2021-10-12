library(ggplot2)

file.wbump <- 'C:\\Users\\31642\\Documents\\Utrecht\\IceClimate\\Project\\SIA-Model\\glacier_bump.csv'
file.flat <- 'C:\\Users\\31642\\Documents\\Utrecht\\IceClimate\\Project\\SIA-Model\\glacier_no_bump.csv'

data.bump <- read.csv(file.wbump)
data.flat <- read.csv(file.flat)


plot.wbump <- ggplot(data = data.bump, aes(x = dl_f, y = t.response)) + geom_line()
plot.flat <- ggplot(data = data.flat, aes(x = dl_f, y = t.response)) + geom_line()

df.tot <- rbind(data.bump, data.flat)

plot.total <- (ggplot(data = df.tot, aes(x=h.ela, y = t.response, color = dl_f, shape = bump))
               + geom_point(size = 3) + geom_line() + ggtitle('response time vs equilibrium line height')   
               + scale_y_continuous(trans = 'log2'))
print(plot.total)