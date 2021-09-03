library('geobr')
library('readr')
library('sf')
library("leaflet")
library(tidyr)
library(dplyr)
library(stringr)

rs <- read_municipality(code_muni= "RS", year=2020)
dados_vac <- read_csv("~/Mapa RS - Vacinação/dados_vac.csv")
dados_vac <- dados_vac %>% separate('municipio', c("cod_municipio", "nome_municipio"), sep =" - ")
dados_vac <- dados_vac %>% separate('porcent_esquema_vacinal_completo', c("porcent_esquema_vacinal_completo", "numero_bruto_esquema_vacinal_completo"), sep ="% ")
dados_vac$porcent_esquema_vacinal_completo <- as.numeric(dados_vac$porcent_esquema_vacinal_completo)

rs$code_muni <- substr(rs$code_muni,1,6)
dataset_final = left_join(rs, dados_vac, by=c("code_muni"= "cod_municipio"))

map <- st_as_sf(dataset_final)
map <- st_transform(map, "+init=epsg:4326")
bins <- c(10, 30, 50, 70, 90)
custom <- c('#ffffd4','#fed98e','#fe9929','#d95f0e','#993404')
pal <- colorBin(palette = custom, domain = map$porcent_esquema_vacinal_completo, bins = bins)

labels <- sprintf(
  "<strong>%s</strong><br/>Esquema vacinal completo em: %s",
  map$nome_municipio, map$porcent_esquema_vacinal_completo
) %>% lapply(htmltools::HTML)

leaflet(map) %>%
  addTiles() %>%
  addPolygons(
    fillColor = ~ pal(porcent_esquema_vacinal_completo),
    weight = 0.5,
    opacity = 1,
    color = "gray",
    dashArray = "3",
    fillOpacity = 0.9,
    highlight = highlightOptions(
      weight = 5,
      color = "#666",
      dashArray = "",
      fillOpacity = 0.7,
      bringToFront = TRUE),
    label = labels,
    labelOptions = labelOptions(
      style = list("font-weight" = "normal", padding = "3px 8px"),
      textsize = "15px",
      direction = "auto")
  ) %>%
  addLegend(pal = pal, values = ~porcent_esquema_vacinal_completo, opacity = 1, 
            position = "bottomright",
            title = "Esquema Vacinal completo Covid 2021 no RS (%)")