require "gui.require"
require "gui.mapping"

local Validation = true
local e
local w
local wc

function Main.prepare()
          Main.e = Jkr.CreateEventManager()
          Engine:Load(Validation)
          Main.FrameSize = vec2(1920 / 2, 1080 / 2)
          Main.w = Jkr.CreateWindow(Engine.i, "GUI", nil, 4, Main.FrameSize)
          Main.wr_ = Jkr.CreateGeneralWidgetsRenderer(nil, Engine.i, Main.w, Main.e)
          Main.wc = vec4(0.2)
          Main.baseDepth = 50
          Main.__prepared = true

          e = Main.e
          w = Main.w
          wc = Main.wc
          Main.mapping_prepare()
end

function Main.main()
          if not Main.__prepared then
                    Main.prepare()
          end
          while not e:ShouldQuit() do
                    Main.mapping_update()

                    e:ProcessEventsEXT(w)
                    w:Wait()
                    w:AcquireImage()
                    w:BeginRecording()

                    Main.mapping_dispatch()

                    w:BeginUIs()
                    Main.mapping_draw()
                    w:EndUIs()

                    w:BeginDraws(wc.x, wc.y, wc.z, wc.w, 1)
                    w:ExecuteUIs()
                    w:EndDraws()

                    w:BlitImage()
                    w:EndRecording()

                    w:Present()
          end
end

return Main
