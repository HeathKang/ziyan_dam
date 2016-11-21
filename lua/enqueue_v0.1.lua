
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

    if old_timestamp == false then
        redis.call("HSET",eqpt_key,"timestamp",timestamp)
        old_timestamp = redis.call("HGET",eqpt_key,"timestamp")
    end

    if timestamp - old_timestamp > 15 then

        old_timestamp =  redis.call("HSET",eqpt_key,"timestamp",timestamp)

        local s = {
                cmd = ARGV[2],
                rawdata = rawdata,
                data = {
                    measurement = measurement,
                    time = timestamp,
                    fields = {
                        temp  = vdata
                              },
                    tags = {
                        eqpt_no =  eqt,
                        node = "1"
                            }
                }
            }

        local msg = cmsgpack.pack(s)  -- pack msg

        redis.call("RPUSH", "data_queue",msg) -- msg queue

        return s
    end



