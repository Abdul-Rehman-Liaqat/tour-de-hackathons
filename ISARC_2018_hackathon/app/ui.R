ui <- fluidPage(
  
  # Page title
  titlePanel("US State Energy Profiles"),
  
  # Link to source data
  helpText( "Source data provided by the "
            , a("US Energy Information Administration", href = "http://www.eia.gov/state/")
            , "."
  ),
  
  # Sidebar with controls
  sidebarLayout( sidebarPanel( selectInput( inputId = 'variable' 
                                            , label   = "Choose a variable"
                                            , choices = list()  # place holder!
  )
  )
  
  # Leaflet map
  , mainPanel( leafletOutput( outputId = 'map') )
  )
  
)