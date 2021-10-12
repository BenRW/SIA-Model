library(ggplot2)

file.rt_b <- 'C:\\Users\\31642\\Documents\\Utrecht\\IceClimate\\Project\\SIA-Model\\glacier_bump_1.csv'
file.rt_nb <- 'C:\\Users\\31642\\Documents\\Utrecht\\IceClimate\\Project\\SIA-Model\\glacier_no_bump_1.csv'

file.mass_b <- 'C:\\Users\\31642\\Documents\\Utrecht\\IceClimate\\Project\\SIA-Model\\mass_bump.csv'
file.mass_nb <- 'C:\\Users\\31642\\Documents\\Utrecht\\IceClimate\\Project\\SIA-Model\\mass_no_bump.csv'

dat.rt_b <- read.csv(file.rt_b)
dat.rt_nb <- read.csv(file.rt_nb)
dat.mass_nb <- read.csv(file.mass_nb)
dat.mass_b <- read.csv(file.mass_b)

plot.mass <- (ggplot() + geom_line(data = dat.mass_b, aes(x = time, y = mass))
+ geom_line(data = dat.mass_nb, aes(x = time, y = mass), color = 'red'))