from visualizations.crash_by_period_vis import CrashByPeriodTrends 
from visualizations.cyc_ped__accidents_vis  import PedestriansAccidentsGraphs
from visualizations.cyc_ped__accidents_vis  import PedestriansAccidents
from visualizations.liscense_status_vis  import LiscenseStatusTrends
from visualizations.position_lethality_vis import CarSeatDangers
from visualizations.seasonal_alcohol  import SeasonalAlcoholColissions

crash_period_trends = CrashByPeriodTrends()
ped_accidents_plots = PedestriansAccidentsGraphs()
ped_accidents_map = PedestriansAccidents()
license_status_trends = LiscenseStatusTrends()
car_seat_danger = CarSeatDangers()
seasonal_alcohol = SeasonalAlcoholColissions()

crash_period_trends.crash_by_period_plot()
ped_accidents_plots.accidents_graphs_plot()
ped_accidents_map.plot_accidents()
license_status_trends.pie_chart_borough_collision_composition()
license_status_trends.pie_chart_borough_license_composition()
license_status_trends.scatter_plot()
car_seat_danger.show_graph()
seasonal_alcohol.graph_plotting()


