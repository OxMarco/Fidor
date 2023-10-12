import asyncio
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='0zf0iykby281ec56z4d1yp05rf48lfk2mol5nyhr3fmqngdc')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('test-main.h0eqnttg2w.viam.cloud', opts)

async def main():
    robot = await connect()
    my_camera = Camera.from_robot(robot=robot, name="webcam")
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())
