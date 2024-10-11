from bilinovel import downloader_router
# from common.log import init_log

# init_log("logs")

# downloader_router(
#     root_path="out", book_no="3410", volume_no="11", color_chap_name="作品相关"
# )

volumes = ",".join([str(i) for i in range(4, 11)]+[12])
# volumes = '3'

downloader_router(
    root_path="out", book_no="3410", volume_no=volumes, color_chap_name="作品相关"
)
