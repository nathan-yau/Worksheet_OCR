import cv2


def define_range(df, sheet_number, edge_coordinates, result_image):
    pxs, pxe, pys, pye = edge_coordinates[0], edge_coordinates[1], edge_coordinates[2], edge_coordinates[3]
    df_row = (df.loc[df['shnum'] == sheet_number])
    x_region_list = [pxs +30, pxs + int((pxe - pxs - 40) / 2), pxe - 30]
    y_region_list = [list(map(int, df_row.iloc[:, 2 + g * 4:(g + 1) * 4 + 2].values.tolist()[0])) for g in
                     range(int(df_row.region_num.values))]
    num_count = 30
    for u in range(len(y_region_list)):
        for x in range(y_region_list[u][0]):
            for r in range(y_region_list[u][1]):
                value = df_row.iloc[:, num_count].values
                (wt, ht), _ = cv2.getTextSize(str(value), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                cv2.putText(img=result_image, text=str(value).replace("'", ""),
                            org=(x_region_list[x * 2]+(wt*(x-1)),
                                 pys + (y_region_list[u][2] + y_region_list[u][3] * (r + 1)) - ht),
                            fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(0, 0, 255), thickness=5)
                cv2.putText(img=result_image, text=str(value).replace("'", ""),
                            org=(x_region_list[x * 2]+(wt*(x-1)),
                                 pys + (y_region_list[u][2] + y_region_list[u][3] * (r + 1)) - ht),
                            fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
                num_count += 1
                if y_region_list[u][0] == 1:
                    cv2.rectangle(result_image, (x_region_list[0], pys + (y_region_list[u][2])),
                                 (x_region_list[2], pys + (y_region_list[u][2] + y_region_list[u][3] * (r + 1))),
                                 (255, 0, 0), 1)
                elif y_region_list[u][0] == 2 and x == 0:
                    cv2.rectangle(result_image, (x_region_list[0], pys + (y_region_list[u][2])),
                                 (x_region_list[1], pys + (y_region_list[u][2] + y_region_list[u][3] * (r + 1))),
                                 (0, 0, 255), 1)
                elif y_region_list[u][0] == 2 and x == 1:
                    cv2.rectangle(result_image, (x_region_list[1], pys + (y_region_list[u][2])),
                                 (x_region_list[2], pys + (y_region_list[u][2] + y_region_list[u][3] * (r + 1))),
                                 (0, 255, 0), 1)
    return result_image
