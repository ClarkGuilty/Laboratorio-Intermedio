function [PHASE,TRANS0,TRANS1] = yakuscript( RAWr_TH0 , BHC_TH0 , Params_TH0 , RAWr_TH1 , BHC_TH1 , Params_TH1 , h , maxIters )
%function [PHASE,TRANS0,TRANS1] = yakuscript( RAWr_TH0 , BHC_TH0 , Params_TH0 , RAWr_TH1 , BHC_TH1 , Params_TH1 , h , maxIters )
%
%Función que extrae imagenes de Fase y Absorción, aplicando el algoritmo de
%reconstrucción de fase y absorción de rayos X de Jan Yakubek.
%
%Parámetros de entrada para esta función:
%h: Celda con los valores de calibración, en grosor.
%maxIters: número total de iteraciones a realizar.
%RAWr_TH0: Imagen RAW para el umbral bajo, normalizada por tiempo de exp.
%RAWr_TH1: Imagen RAW para el umbral alto, normalizada por tiempo de exp.
%BHC_TH0: Imagen BH-Corrected de la imagen RAW a umbral bajo.
%BHC_TH1: Imagen BH-Corrected de la imagen RAW a umbra alto.
%Params_TH0: Celda con los 3 grupos de parámetros de calibración para todos
%los pixeles del sensor, a bajo umbral.
%Params_TH1: Celda con los 3 grupos de parámetros de calibración para todos
%los pixeles del sensor, a alto umbral.

%INIT

%Se almacenan las imágenes RAW y BH-Corrected originales.
M0 = RAWr_TH0;
M1 = RAWr_TH1;
B0 = BHC_TH0;
B1 = BHC_TH1;

%Se calcula la cantidad de puntos de calibración, según el tamaño de h, la
%celda que contiene los valores (en grosor) de dichos puntos.
calPoints = size(h,2);

%Matriz q, al inicio de las iteraciones es una matriz llena de 1.
q = ones(256,256);

%Inician las iteraciones acá
for n = 1:1:maxIters

%Se calcula el nuevo valor de las imágenes de la iteración n-ésima, según
%los valores para q obtenidos en la iteración previa.
%OJO: Este proceso es destructivo para las imágenes originales. Es
%necesario usar unacopia de las imágenes, si se quieren conservar
%post-procesamiento para comparar.
RAWr_TH0 = RAWr_TH0 .* q;
RAWr_TH1 = RAWr_TH1 .* q;

%Se recorren las dos imágenes, a umbral bajo y alto, y se calcula el
%correspondiente valor de q para cada pixel.
for i = 1:1:256
for j = 1:1:256

    %Encontrar qué ecuación exponencial, de todas las que están definidas
    %por los parámetros de calibración BHC, representa el valor que tiene
    %cada pixel de la imagen, y extraer el valor que retorna dicha función
    %exponencial interpoladora.
    %Proceso realizado para la imagen a bajo y alto umbral (TH0 y TH1).
    for k = 1:1:calPoints-1
        
        flag_TH0 = 0;
        flag_TH1 = 0;
        
        %El pixel tiene un valor que está por debajo del punto de
        %calibración más pequeño (Open Beam). Se modifica el valor del
        %pixel para que sea igual a h{1}
        if BHC_TH0(i,j) < h{1}
            BHC_TH0(i,j) = h{1};
        end
        
        %El pixel tiene un valor que está por encima del punto de
        %calibración más alto. Se modifica el valor del pixel para que sea
        %igual a h{calPoints}.
        if BHC_TH0(i,j) > h{calPoints}
            BHC_TH0(i,j) = h{calPoints};            
        end
        
        
        %Calcular los valores de la función interpoladora C y C', para el
        %umbral TH0, para cada pixel (i,j), de la imagen RAWr_TH0.
        if BHC_TH0(i,j) >= h{k} && BHC_TH0(i,j) < h{k+1} && flag_TH0 == 0
            
            %Cálculo de Y_k y Y_k+1, las correspondientes ratas de conteo
            %que limitan el rango interpolado.            
            y_k = Params_TH0{1}{k}(i,j) * exp( Params_TH0{2}{k}(i,j) * h{k} ) ...
                + Params_TH0{3}{k}(i,j);
            
            y_k1 = Params_TH0{1}{k+1}(i,j) * exp( Params_TH0{2}{k+1}(i,j) * h{k+1} ) ...
                 + Params_TH0{3}{k+1}(i,j);
            
            %Cálculo de C( RAWr_TH0(i,j) ), C'( RAWr_TH0(i,j) )
            %Para esto, se llaman a los parámetros k-ésimo y k+1-ésimo.
            %Si ya se encontró la función interpoladora correcta, no volver
            %a entrar a esta ejecución condicional (flag_TH0 = 1).
            C_RAWr_TH0 = ( ( RAWr_TH0(i,j) - y_k1 ) / ...
                         ( Params_TH0{2}{k}(i,j) * ( y_k - y_k1 ) ) ) * ...
                         log( ( RAWr_TH0(i,j) - Params_TH0{3}{k}(i,j) ) / ...
                         Params_TH0{1}{k}(i,j) ) ...
                         + ...
                         ( ( -RAWr_TH0(i,j) + y_k ) / ...
                         ( Params_TH0{2}{k+1}(i,j) * ( y_k - y_k1 ) ) ) * ...
                         log( ( RAWr_TH0(i,j) - Params_TH0{3}{k+1}(i,j) ) / ...
                         Params_TH0{1}{k+1}(i,j) );
                        
            Cp_RAWr_TH0 = ( log( ( RAWr_TH0(i,j) - Params_TH0{3}{k}(i,j) ) / ...
                          Params_TH0{1}{k}(i,j) ) / ...
                          ( Params_TH0{2}{k}(i,j) * ( y_k - y_k1 ) ) ) ...
                          + ...
                          ( ( RAWr_TH0(i,j) - y_k1 ) / ( Params_TH0{2}{k}(i,j) * ...
                          ( y_k - y_k1 ) * ( RAWr_TH0(i,j) - Params_TH0{3}{k}(i,j)  ) ) ) ...
                          - ...
                          ( log( ( RAWr_TH0(i,j) - Params_TH0{3}{k+1}(i,j) ) / ...
                          Params_TH0{1}{k+1}(i,j) ) / ...
                          ( Params_TH0{2}{k+1}(i,j) * ( y_k - y_k1 ) ) ) ...
                          + ...
                          ( ( -RAWr_TH0(i,j) + y_k ) / ( Params_TH0{2}{k+1}(i,j) * ...
                          ( y_k - y_k1 ) * ( RAWr_TH0(i,j) - Params_TH0{3}{k+1}(i,j)  ) ) );
                          
                        
            flag_TH0 = 1;
        end

        
        %El pixel tiene un valor que está por debajo del punto de
        %calibración más pequeño (Open Beam). Se modifica el valor del
        %pixel para que sea igual a h{1}
        if BHC_TH1(i,j) < h{1}
            BHC_TH1(i,j) = h{1};
        end
        
        %El pixel tiene un valor que está por encima del punto de
        %calibración más alto. Se modifica el valor del pixel para que sea
        %igual a h{calPoints}.
        if BHC_TH1(i,j) > h{calPoints}
            BHC_TH1(i,j) = h{calPoints};            
        end
        
        
        %Calcular los valores de la función interpoladora C y C', para el 
        %umbral TH1, para cada pixel.
        %Si ya se encontró la función interpoladora correcta, no volver a
        %entrar a esta ejecución condicional (flag_TH1 = 1).
        if BHC_TH1(i,j) >= h{k} && BHC_TH1(i,j) < h{k+1} && flag_TH1 == 0
                        
            %Cálculo de Y_k y Y_k+1, las correspondientes ratas de conteo
            %que limitan el rango interpolado. 
            y_k = Params_TH1{1}{k}(i,j) * exp( Params_TH1{2}{k}(i,j) * h{k} ) ...
                + Params_TH1{3}{k}(i,j);
            
            y_k1 = Params_TH1{1}{k+1}(i,j) * exp( Params_TH1{2}{k+1}(i,j) * h{k+1} ) ...
                 + Params_TH1{3}{k+1}(i,j);
            
            
            %Cálculo de C( RAWr_TH1(i,j) ), C'( RAWr_TH1(i,j) )
            %Para esto, se llaman a los parámetros k-ésimo y k+1-ésimo.
            C_RAWr_TH1 = ( ( RAWr_TH1(i,j) - y_k1 ) / ...
                         ( Params_TH1{2}{k}(i,j) * ( y_k - y_k1 ) ) ) * ...
                         log( ( RAWr_TH1(i,j) - Params_TH1{3}{k}(i,j) ) / ...
                         Params_TH1{1}{k}(i,j) ) ...
                         + ...
                         ( ( -RAWr_TH1(i,j) + y_k ) / ...
                         ( Params_TH1{2}{k+1}(i,j) * ( y_k - y_k1 ) ) ) * ...
                         log( ( RAWr_TH1(i,j) - Params_TH1{3}{k+1}(i,j) ) / ...
                         Params_TH1{1}{k+1}(i,j) );
            
            Cp_RAWr_TH1 = ( log( ( RAWr_TH1(i,j) - Params_TH1{3}{k}(i,j) ) / ...
                          Params_TH1{1}{k}(i,j) ) / ...
                          ( Params_TH1{2}{k}(i,j) * ( y_k - y_k1 ) ) ) ...
                          + ...
                          ( ( RAWr_TH1(i,j) - y_k1 ) / ( Params_TH1{2}{k}(i,j) * ...
                          ( y_k - y_k1 ) * ( RAWr_TH1(i,j) - Params_TH1{3}{k}(i,j)  ) ) ) ...
                          - ...
                          ( log( ( RAWr_TH1(i,j) - Params_TH1{3}{k+1}(i,j) ) / ...
                          Params_TH1{1}{k+1}(i,j) ) / ...
                          ( Params_TH1{2}{k+1}(i,j) * ( y_k - y_k1 ) ) ) ...
                          + ...
                          ( ( -RAWr_TH1(i,j) + y_k ) / ( Params_TH1{2}{k+1}(i,j) * ...
                          ( y_k - y_k1 ) * ( RAWr_TH1(i,j) - Params_TH1{3}{k+1}(i,j)  ) ) );
                        
            flag_TH1 = 1;
        end

    end
    
    %Cambio el valor de q para el pixel (i,j), según lo calculado
    %previamente.
    q(i,j) = 1 - ( C_RAWr_TH0 - C_RAWr_TH1 ) /...
                 ( RAWr_TH0(i,j) * Cp_RAWr_TH0 - RAWr_TH1(i,j) * Cp_RAWr_TH1 );
    
        
end
end

end


%Construcción de resultados
PHASE = 1./q - 1;
TRANS0 = M0 ./ ( 1 + PHASE ); %OJO! Si es RAWr_TH0? Por qué no es RAWr_TH1?
TRANS1 = M1 ./ ( 1 + PHASE ); %OJO! Si es RAWr_TH0? Por qué no es RAWr_TH1?

end
