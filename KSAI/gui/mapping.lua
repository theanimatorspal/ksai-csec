require "gui.require"
Main.NodeTitleTextColor = vec4(0, 0, 0, 1)
Main.NodeTitleBackColor = vec4(0.7, 0.7, 0.7, 1)
Main.ContentBackColor = vec4(0)

local e
local w
local wc
local wr_
local cimage
local ipainter
local ipainter_clear
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
                    local n    = {}
                    n.p        = p or vec3(Main.FrameSize.x / 2.0, Main.FrameSize.y / 2.0, Main.baseDepth)
                    local Dims = Main.font:GetTextDimension(name)
                    n.d        = d or vec3(Dims.x + 10, Dims.y, 1)
                    n.name     = name
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


          do
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
          end

          do
                    ipainter = Jkr.CreateCustomImagePainter("cache2/ImagePainterCache", TwoDimensionalIPs.Line.str)
                    ipainter:Store(Engine.i, w)
                    cimage.RegisterPainter(ipainter)

                    ipainter_clear = Jkr.CreateCustomImagePainter("cache2/ImagePainterClearCache",
                              TwoDimensionalIPs.Clear.str)
                    ipainter_clear:Store(Engine.i, w)
          end

          do
                    local node1 = Node.Add(Node.New(vec3(100, 100, Main.baseDepth), nil, "main"))
                    local node2 = Node.Add(Node.New(nil, nil, "non_main"))
                    Node.AddConnection(vec2(node1.id, node2.id))
          end
end

Main.mapping_draw = function()
          wr_:DrawExplicit(scissorsToDraw)
end

Main.mapping_dispatch = function()
          ipainter_clear:Bind(w, Jkr.CmdParam.None)
          ipainter_clear:BindImageFromImage(w, cimage, Jkr.CmdParam.None)
          ipainter:Draw(w,
                    Jkr.Matrix2CustomImagePainterPushConstant(),
                    math.ceil(Main.FrameSize.x / 16),
                    math.ceil(Main.FrameSize.y / 16),
                    1,
                    Jkr.CmdParam.None)

          ipainter:Bind(w, Jkr.CmdParam.None)
          ipainter:BindImageFromImage(w, cimage, Jkr.CmdParam.None)
          for i, value in ipairs(Connections) do
                    local n1 = Nodes[value.x]
                    local n2 = Nodes[value.y]
                    local left, right, top, bottom

                    if n1.p.x < n2.p.x then
                              left = n1.p.x + n1.d.x / 2.0
                              right = n2.p.x + n2.d.x / 2.0
                    else
                              left = n2.p.x + n2.d.x / 2.0
                              right = n1.p.x + n1.d.x / 2.0
                    end

                    if n1.p.y < n2.p.y then
                              top = n1.p.y + n1.d.y / 2.0
                              bottom = n2.p.y + n2.d.y / 2.0
                    else
                              top = n2.p.y + n2.d.y / 2.0
                              bottom = n1.p.y + n1.d.y / 2.0
                    end

                    local pos_dimen = vec4(left, top, math.abs(right - left), math.abs(bottom - top))
                    local pconst = Jkr.Matrix2CustomImagePainterPushConstant()
                    pconst.a = mat4(pos_dimen, vec4(0), vec4(0), vec4(0))
                    ipainter:Draw(w,
                              pconst,
                              math.ceil(pos_dimen.z / 16),
                              math.ceil(pos_dimen.w / 16),
                              1,
                              Jkr.CmdParam.None)
          end

          cimage.CopyToSampled(simage)
          wr_:Dispatch()
end

Main.mapping_update = function()
          for i, _ in ipairs(NodesToDraw) do
                    local widget = WidgetsForNodes[i]
                    local value = Nodes[NodesToDraw[i].id]
                    if not widget then
                              WidgetsForNodes[i] = wr_.CreateMovableButton(
                                        value.p,
                                        value.d,
                                        Main.font,
                                        value.name,
                                        Main.NodeTitleTextColor,
                                        Main.NodeTitleBackColor
                              )
                              value.Widget = WidgetsForNodes[i]
                    else
                              local dim = Main.font:GetTextDimension(value.name)
                              if dim.x > value.d.x then
                                        value.d.x = dim.x + 10
                                        value.d.y = 0
                                        widget:Update(widget.mCurrentPosition, value.d)
                              end
                              value.p = widget.mCurrentPosition
                              value.d = widget.mCurrentDimension
                    end
          end
          wr_:Update()
end
