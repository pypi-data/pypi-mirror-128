# TA-CMI
A Python wrapper to read out  sensors from Technische Alternative using the C.M.I.

## How to use package

```python
import asyncio

from ta_cmi import CMI, Languages, ApiError, RateLimitError, InvalidCredentialsError


async def main():
    try:
        cmi = CMI("http://192.168.1.101", "admin", "admin")

        devices = await cmi.getDevices()

        device = devices[0]

        await device.update()

        print(str(device))

        inputChannels = device.inputs
        outputChannels = device.outputs

        for i in inputChannels:
            ch = inputChannels.get(i)
            print(str(ch))

        for o in outputChannels:
            ch = outputChannels.get(o)
            print(f"{str(ch)} - {ch.getUnit(Languages.DE)}")
    except (ApiError, RateLimitError, InvalidCredentialsError) as error:
        print(f"Error: {error}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
```