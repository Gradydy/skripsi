import vrp
import pandas as pd
df = pd.DataFrame({'coor_x':[-22.98, -22.97, -22.92, -22.87, -22.89], 'coor_y': [-43.19, -43.39, -43.24, -43.28, -43.67]})
hasil = vrp.main(df,2)
print(hasil)
