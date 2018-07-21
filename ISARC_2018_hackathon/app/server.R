library(shiny)
library(leaflet)
library(maps)
server <- function(input, output) {
  output$message <- renderText({ "Hello world!" })
}
