INSERT INTO public.phrases_in_xml(xml_id,phrase)
SELECT public.brandbankxml.xml_id, "Phrase"
FROM public.brandbankxml
JOIN public."phrases"
ON public.brandbankxml.text LIKE '%' || "Phrase" || '%';