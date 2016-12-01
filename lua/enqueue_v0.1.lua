
--[[

for DAM

]]
-- key1,argv1,argv2,argv3,argv4
-- KEYS[1], equipment
-- ARGV[1], timestamp
-- ARGV[2], cmd
-- ARGV[3], measurement
-- ARGV[4], data
-- ARGV[5], rawdata

-- eqpt_no,timestamp, cmd, measurement, data, rawdata

    local eqt = KEYS[1]
    local timestamp = ARGV[1]
    local cmd = ARGV[2]
    local measurement = ARGV[3]
    local vdata =cmsgpack.unpack(ARGV[4])
    local rawdata = cmsgpack.unpack(ARGV[5])

    local eqpt_key = string.format("%s_%s",KEYS[1],ARGV[2])

    local old_timestamp = redis.call("HGET", eqpt_key,"timestamp")

    local switch = {
            ["1"] = "hpu_6",
            ["2"] = "hpu_5",
            ["3"] = "hpu_4",
            ["4"] = "hpu_3",
            ["5"] = "hpu_2",
            ["6"] = "hpu_1"
    }


    if old_timestamp == false then
        redis.call("HSET",eqpt_key,"timestamp",timestamp)
        old_timestamp = redis.call("HGET",eqpt_key,"timestamp")
    end

    if timestamp - old_timestamp > 15 then

        old_timestamp =  redis.call("HSET",eqpt_key,"timestamp",timestamp)

        local s = {
                cmd = ARGV[2],
                rawdata = rawdata[0],
                data = {
                    measurement = measurement,
                    time = timestamp,
                    fields = {
                        temp_01  = vdata[1],
                        temp_02  = vdata[2],
                        temp_03  = vdata[3],
                        temp_04  = vdata[4],

                        pd_01 = vdata [5],
                        pd_02 = vdata[6],
                        pd_03 = vdata[7],

                        as_temp = vdata [8],
                        as_saturation = vdata[9]


                              },
                    tags = {
                        eqpt_no = switch[eqt],
                        node = "1"
                            }
                }
            }

        local msg = cmsgpack.pack(s)  -- pack msg

        redis.call("RPUSH", "data_queue",msg) -- msg queue

        return s
    end



