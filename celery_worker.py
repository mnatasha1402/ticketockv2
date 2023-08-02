from celery import Celery


# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['result_backend'],
#         broker=app.config['broker_url']
#     )
#     # celery.conf.update(app.config["CELERY_CONFIG"])
#     celery.conf.update(include='CELERY_INCLUDE')
#     celery.conf.update(app.config)
    

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery

# # celery_inst = make_celery(app)

app = Celery('myapp', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

app.conf.update(
    task_default_queue='mail',
    smtp_host='localhost',
    smtp_port=1025,
    smtp_user='nats@email.com',
    smtp_password='',
    smtp_tls=True,
)