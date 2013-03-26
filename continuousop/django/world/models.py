from django.db import models


import logging
logger = logging.getLogger(__file__)


class Place(models.Model):
    name = models.TextField()
    tags = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images", blank=True, null=True)

    pose_x = models.FloatField(blank=True, null=True)
    pose_y = models.FloatField(blank=True, null=True)
    pose_angle = models.FloatField(blank=True, null=True)

    map_x = models.IntegerField(blank=True, null=True)
    map_y = models.IntegerField(blank=True, null=True)
    map_width = models.IntegerField(blank=True, null=True)
    map_height = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class Camera(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=512)

    # Features this camera is available for. It consists of a string of single
    # space separated words, each a feature identifier (e.g. "look pick-up").
    features = models.CharField(max_length=512, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.url)


class RobotManager(models.Magnager):

    def current(self):
        try:
            return super(RobotManager, self).get(is_current=True)
        except self.model.DoesNotExist:
            msg = 'No current robot! At least one robot must be "current"'
            logger.error(msg)
            raise self.model.DoesNotExist(msg)
        except self.model.MultipleObjectsReturned:
            msg = 'More that one robot is "current"!'
            logger.error(msg)
            raise self.model.MultipleObjectsReturned(msg)


class Robot(models.Model):
    objects = RobotManager()

    name = models.CharField(max_length=50, blank=True)
    tags = models.TextField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="images", blank=True, null=True)

    public = models.BooleanField(default=False)

    state = models.IntegerField(choices=(
        (0, 'Idle'), (1, 'Busy'),
    ))

    # URL to robot's rosbridge instance
    service_url = models.CharField(max_length=512)

    camera_base_url = models.CharField(max_length=128)
    cameras = models.ManyToManyField(Camera)

    # The multi_ros prefix string for topics to forward.
    multi_ros_prefix = models.CharField(max_length=50, blank=True)

    "Do not use this field directly. Use set_current() instead."
    is_current = models.BooleanField(default=False)

    def set_current(self):
        "Saves this instance as the current robot."
        try:
            current = self.objects.current()
            current.is_current = False
            current.save()
        except Robot.DoesNotExist:
            # Set this as the only current.
            logger.warn('There is no current robot. Fixing it.')
        except Robot.MultipleObjectsReturned:
            # Set all of those as not current
            logger.warn('Multiple robots set as current. Fixing it.')
            self.objects.filter(is_current=True).update(is_current=False)
        self.is_current = True
        self.save()

    def __unicode__(self):
        return self.name
