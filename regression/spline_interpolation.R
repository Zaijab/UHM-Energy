library(mgcv)
library(splines)
library(ggplot2)
library(lubridate)

data <- read.csv("data.csv")

yhour <- function(time) {
  (as.integer(format(time, '%j')) - 1) * 96 + as.integer(format(time, '%H'))
}

dense <- seq(as.POSIXct('2021-07-07 00:00:00'), as.POSIXct("2022-06-13 23:45:00"), by = 900)
dense <- yhour(dense)

# Generate dow : hod : hoy : temperature_c for test data from GIS.

knots_1 <- 8
knots_2 <- 8
model <- lm(log(kw_average) ~ ns(hod, df = knots_1)*ns(hoy, df = knots_2)*factor(dow) + ns(temperature_c), data = data)

data$predictions <- predict(model)
data$log_power <- log(data$kw_average)

plot(x = factor(data$hoy, levels = c(data$hoy)), y = data$log_power, pch = '.', col = 'red', xaxt = 'n') +
    lines(x = dense, y = predict(model, newdata = dense), pch = '.', col='blue')


plot(x = dense, y = predict(model, newdata = dense), pch = '.', col='blue')
