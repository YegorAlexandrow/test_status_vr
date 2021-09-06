from pydantic import BaseModel, Field

from typing import List

import redis
import time
import numpy as np


_redis_conn = redis.Redis(
    host='localhost',
    port=6379,
    password='DTL@b2021',
    db=0
)


class Position(BaseModel):
    x: float = 0
    y: float = 0
    z: float = 0


class Rotation(BaseModel):
    r: float = 0
    p: float = 0
    y: float = 0


class Pose(BaseModel):
    pos: Position = Position()
    rot: Rotation = Rotation()


class WheelsStatusSchema(BaseModel):
    status: str = 'OK'
    v: float = Field(0.0, description='Linear speed, m/s')
    w: float = Field(0.0, description='Angular speed, deg/s')


class HeadStatusSchema(BaseModel):
    status: str = 'OK'
    pose: Pose = Pose()


class ArmPoseSchema(BaseModel):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    yaw: float = 0.0


class ArmStatusSchema(BaseModel):
    status: str = 'OK'
    gripper_angle = Field(0.0, description='???')
    gripper_effort = Field(0.0, description='???')
    weight = Field(0.0, description='The weight of the object in the gripper')
    range = Field(0.0, description='???')
    target_pose: Pose = Pose()
    poses: List[Pose] = Field(
        [],
        description='shoulder, elbow, gripper'
    )


class RobotStatusSchema(BaseModel):
    robot_state: str
    battery = Field(1.0, description='Battery charge')
    mic = Field(False, description='Microphone on/off')
    head: HeadStatusSchema
    wheels: WheelsStatusSchema
    arms: List[ArmStatusSchema]


_l_base = np.array([-200, 0, -100])
_r_base = np.array([200, 0, -100])

while True:
    for st in ('ARM_OPERATING_ST',):
        for i in range(100):
            alpha = i / 100 * 6.28
            _l_arm = np.array([-200, 300, -1 * i]) + np.array([np.cos(alpha), np.sin(alpha), 0]) * 200
            _r_arm = np.array([200, 300, -1 * i]) + np.array([np.cos(-alpha), np.sin(-alpha), 0]) * 99

            _l_mid = (_l_base + _l_arm) * 0.5
            _r_mid = (_r_base + _r_arm) * 0.5

            status = RobotStatusSchema(
                robot_state=st,
                battery=i / 100,
                mic=i > 50,
                wheels={
                    'status': 'OK',
                    'v': i / 100 * 2,
                    'w': i / 100 * 180 - 90
                },
                head={
                    'status': 'OK',
                    'pose': {'rot': {'y': i / 100 * 180 - 90}}
                },
                arms=[
                    {
                        'status': 'OK',
                        'gripper_angle': i / 100,
                        'gripper_effort': i / 100,
                        'range': i / 100,
                        'weight': i * 8,
                        'target_pose': {'pos': {k: v*1.01 for k, v in zip('xyz', _l_arm)}, 'rot': {}},
                        'poses': [
                            {'pos': {k: v for k, v in zip('xyz', _l_base)}, 'rot': {}},
                            {'pos': {k:v for k, v in zip('xyz', _l_mid)}, 'rot': {}},
                            {'pos': {k:v for k, v in zip('xyz', _l_arm)},
                             'rot': {'y': alpha / 3.14 * 180}},
                        ],
                    },
                    {
                        'status': 'OK',
                        'gripper_angle': i / 100,
                        'gripper_effort': i / 100,
                        'range': i / 100,
                        'weight': i * 8,
                        'target_pose': {'pos': {k: v*1.01 for k, v in zip('xyz', _r_arm)}, 'rot': {}},
                        'poses': [
                            {'pos': {k: v for k, v in zip('xyz', _r_base)}, 'rot': {}},
                            {'pos': {k:v for k, v in zip('xyz', _r_mid)}, 'rot': {}},
                            {'pos': {k:v for k, v in zip('xyz', _r_arm)},
                             'rot': {'y': -alpha / 3.14 * 180}},
                        ]
                    }
                ]
            )

            time.sleep(0.1)
            print(status)
            _redis_conn.publish('status', status.json())
