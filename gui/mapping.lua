require "gui.require"
Main.NodeTitleTextColor = vec4(0, 0, 0, 1)
Main.NodeTitleBackColor = vec4(0.7, 0.7, 0.7, 1)
Main.ContentBackColor = vec4(0)

local e
local w
local wc
local wr_
local cimage
local simage
local connectionsQuad
local pconstant
local mainScissor
local scissorsToDraw


local Connections = {}
local Nodes = {}
local NodesToDraw = {}
local WidgetsForNodes = {}

local Node = { --namespace
          New = function(p, d, name)
                    local n = {}
                    n.p     = p or vec3(Main.FrameSize.x / 2.0, Main.FrameSize.y / 2.0, Main.baseDepth)
                    n.d     = d or vec3(0)
                    n.name  = name
                    return n
          end,
          Add = function(inNode)
                    Nodes[#Nodes + 1] = inNode
                    NodesToDraw[#NodesToDraw + 1] = inNode
                    inNode.id = #Nodes
                    return inNode
          end,
          Remove = function()

          end,
          AddConnection = function(inVec2)
                    Connections[#Connections + 1] = inVec2
                    return #Connections
          end,
          RemoveConnection = function()

          end
}

Main.mapping_prepare = function()
          e = Main.e
          w = Main.w
          wc = Main.wc
          wr_ = Main.wr_
          local frameSize_3f = vec3(Main.FrameSize.x, Main.FrameSize.y, 1)

          mainScissor = wr_.CreateScissor(vec3(0), frameSize_3f)
          wr_.SetCurrentScissor(mainScissor)
          scissorsToDraw = {}
          scissorsToDraw[#scissorsToDraw + 1] = mainScissor

          Main.font = wr_.CreateFont("Laila.ttf", 16)
          pconstant = Jkr.Matrix2CustomImagePainterPushConstant()
          pconstant.a = mat4(vec4(1), vec4(1), vec4(1), vec4(1))
          cimage = wr_.CreateComputeImage(vec3(0), frameSize_3f)
          simage = wr_.CreateSampledImage(vec3(0, 0, Main.baseDepth), frameSize_3f)
          connectionsQuad = wr_.CreateQuad(vec3(0, 0, Main.baseDepth + 50), frameSize_3f,
                    pconstant, "showImage", simage.mId)

          local node1 = Node.Add(Node.New(vec3(100, 100, Main.baseDepth), nil, "main"))
          local node2 = Node.Add(Node.New(nil, nil, "non_main"))
          Node.AddConnection(vec2(node1.id, node2.id))
end

Main.mapping_draw = function()
          wr_:DrawExplicit(scissorsToDraw)
end

Main.mapping_dispatch = function()
          wr_:Dispatch()
          cimage.CopyToSampled(simage)
end

Main.mapping_update = function()
          for i, value in ipairs(NodesToDraw) do
                    local widget = WidgetsForNodes[i]
                    if not widget then
                              WidgetsForNodes[i] = wr_.CreateWindowScissor(
                                        value.p,
                                        value.d,
                                        Main.font,
                                        value.name,
                                        Main.NodeTitleTextColor,
                                        Main.NodeTitleBackColor,
                                        Main.ContentBackColor,
                                        true)
                              value.Widget = WidgetsForNodes[i]
                    else
                              local dim = Main.font:GetTextDimension(value.name)
                              if dim.x > value.d.x then
                                        value.d.x = dim.x + 10
                                        value.d.y = dim.y + 5
                                        widget:Update(widget.mCurrentPosition, value.d)
                              end
                    end
          end
          wr_:Update()
end
